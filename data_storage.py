import asyncio
import datetime
import json
from os import path
from typing import Optional

from fastapi_socketio import SocketManager

from config.const import DIR_DATA_MESSAGES, DIR_DATA_ANALYTICS
from services.cache import (
  load_data,
  generate_time_series,
  get_messages_metrics,
  get_time_serie_num_messages,
  prepare_daily_data
)
from services.framework_analytics.data_analytics import DataAnalytics
from services.framework_scraping.data_processing import DataProcessing
from services.framework_scraping.time_series_fetcher import PriceTimeSeries
from services.framework_scraping.tools.missing_dates import get_missing_dates


async def fetch_time_series(start_date, end_date):
  price_series = PriceTimeSeries(
    start_date,
    end_date,
    DIR_DATA_ANALYTICS,
    ["Compra", "Venta"],
    currency="USD",
  )
  await price_series.sync_time_series()


async def async_enumerate(iterable):
  index = 0
  async for item in iterable:
    yield index, item
    index += 1


async def sync_data(missing_dates):
  if len(missing_dates) > 0:
    
    fetcher = DataProcessing(dates=missing_dates, currency="USD")
    
    async for index, complete_date in async_enumerate(fetcher.do_process_messages()):
      print(f'done {complete_date}')
      yield ((index + 1) / len(missing_dates)) * 100  # percent_completed


def update_files():
  analytics = DataAnalytics.do_analytics(DIR_DATA_MESSAGES)
  analytics.dataframe.to_pickle(f"{DIR_DATA_ANALYTICS}/analytics.pickle")
  with open(path.join(DIR_DATA_ANALYTICS, "all_orders.json"), 'w') as file:
    file.write(json.dumps(analytics.orders))


class DataStorage:
  __reporter_dates = None
  
  def reload_from_file(self):
    print("getting missing dates")
    self.__reporter_dates = get_missing_dates(DIR_DATA_MESSAGES)
    print("loading data")
    try:
      self.analytics, self.series = load_data(DIR_DATA_ANALYTICS)
    except FileNotFoundError as e:
      print("no hay ficheros para cargar ... por favor sincronice o cargue los datos")
      return
    self.price_series, self.volumes_series = generate_time_series(self.analytics, self.series)
    
    (
      self.avg_daily_messages,
      _,
      _,
      self.percent_compra,
      self.percent_venta,
    ) = get_messages_metrics(self.analytics)
    
    self.number_messages = get_time_serie_num_messages(self.analytics)
    self.daily_data = prepare_daily_data(self.analytics)
  
  def __init__(self, socket_manager=None):
    self.__background_task = False
    self.websocket_clientes = set()
    self.socket_manager: Optional[SocketManager] = socket_manager
    self.avg_daily_messages = None
    self.percent_compra = None
    self.percent_venta = None
    self.price_series = None
    self.volumes_series = None
    self.analytics = None
    self.series = None
    self.number_messages = None
    self.daily_data = None
    self.reload_from_file()
    self.global_state = None
    self.update_global_state()
  
  def update_global_state(self):
    self.global_state = str(datetime.datetime.now())
  
  @property
  def background_task(self):
    return self.__background_task
  
  async def update_background_task_status(self, value):
    if self.__background_task != value:
      self.__background_task = value
      await self.update_status()
  
  @property
  def start_date(self):
    return self.__reporter_dates.start_date
  
  @property
  def end_date(self):
    return self.__reporter_dates.end_date
  
  @property
  def missing_dates(self):
    return [
      day for (day, is_in)
      in self.dates
      if is_in == False
    ]
  
  @property
  def processed_dates(self):
    return [
      day for (day, is_in)
      in self.dates
      if is_in == True
    ]
  
  @property
  def dates(self):
    return self.__reporter_dates.dates
  
  async def update_status(self, /, update=None, socket_id=None):
    if self.socket_manager is None:
      return
    await self.socket_manager.emit(
      "update", [
        self.background_task,
        len(self.missing_dates),
        self.global_state,
      ], namespace="/",
      to=socket_id,
      callback=lambda *args: print(args),
      ignore_queue=True
    )
    await asyncio.sleep(1)
    print("-" * 30)
    print("update: " + str([
      self.background_task,
      len(self.missing_dates),
      self.global_state,
    ]))
    print("-" * 30)
  
  async def sync_data(self):
    print("sync data....")
    self.__reporter_dates = get_missing_dates(DIR_DATA_MESSAGES)  # super importante no quitar!!!
    print(f"Missing dates found: [{', '.join(self.missing_dates)}]")
    
    await self.update_background_task_status(True)
    try:
      await fetch_time_series(self.start_date, self.end_date)
      
      async for update in sync_data(self.missing_dates):
        await self.update_status(update)
      update_files()
      self.reload_from_file()
      await self.update_background_task_status(False)
    except Exception as exception:  # noqa
      self.reload_from_file()
      await self.update_background_task_status(False)
  
  def connect(self, socket_id):
    self.websocket_clientes.add(socket_id)
  
  def disconnect(self, socket_id):
    if socket_id in self.websocket_clientes:
      self.websocket_clientes.remove(socket_id)


data_store = DataStorage()
