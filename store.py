import json
from os import path

from config.const import DIR_DATA_MESSAGES, DIR_DATA_ANALYTICS
from services.cache import (
  load_data,
  load_time_series,
  get_messages_metrics,
  get_time_serie_num_messages,
  prepare_daily_data
)
from services.framework_analytics.data_analytics import DataAnalytics
from services.framework_scraping.data_processing import DataProcessing
from services.framework_scraping.time_series_fetcher import PriceTimeSeries
from services.framework_scraping.tools.missing_dates import get_missing_dates


class DataStore:
  __reporter_dates = None
  
  def reload_from_file(self):
    self.__reporter_dates = get_missing_dates(DIR_DATA_MESSAGES)
    analytics = DataAnalytics(DIR_DATA_MESSAGES)
    analytics.do_analytics()
    analytics.dataframe.to_pickle(f"{DIR_DATA_ANALYTICS}/analytics.pickle")
    
    with open(path.join(DIR_DATA_ANALYTICS, "/all_orders.json"), 'w') as file:
      file.write(json.dumps(analytics.orders))
  
  def __init__(self, socketio):
    self.socketio = socketio
    self.__background_task = False
    self.websocket_clientes = set()
    
    self.reload_from_file()
    self.analytics, self.series = load_data(DIR_DATA_ANALYTICS)
    self.price_series, self.volumes_series = load_time_series(
      self.analytics, self.series
    )
    (
      self.avg_daily_messages,
      _,
      _,
      self.percent_compra,
      self.percent_venta,
    ) = get_messages_metrics(self.analytics)
    
    self.number_messages = get_time_serie_num_messages(self.analytics)
    self.daily_data = prepare_daily_data(self.analytics)
  
  @property
  def background_task(self):
    return self.__background_task
  
  @background_task.setter
  def background_task(self, value):
    self.__background_task = value
    self.update_status()
  
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
  def dates(self):
    return self.__reporter_dates.dates
  
  def update_status(self, socket_id=None):
    self.socketio.emit(
      "update", [
        self.background_task,
        len(self.missing_dates)
      ], namespace="/",
      to=socket_id
    )
    self.socketio.sleep(3)  # Esto es para dar tiempo a que el servidor procese otras peticiones

  
  def sync_data(self):
    print("sync data....")
    self.background_task = True
    
    price_series = PriceTimeSeries(
      self.start_date,
      self.end_date,
      DIR_DATA_ANALYTICS,
      ["Compra", "Venta"],
      currency="USD",
    )
    price_series.get_time_series()
    
    if len(self.missing_dates) > 0:
      print(f"Missing dates found: {','.join(self.missing_dates)}")
      
      fetcher = DataProcessing(end_dates=self.missing_dates, currency="USD")
      for index, complete_date in enumerate(fetcher.do_process_messages()):
        print(f'done {complete_date}')
        if index % 5 == 0:
          self.reload_from_file()
          self.update_status()
      self.reload_from_file()
    
    self.background_task = False
  
  def connect(self, socket_id):
    self.websocket_clientes.add(
      socket_id
    )
    self.update_status(
      socket_id
    )
  
  def disconnect(self, socket_id):
    self.websocket_clientes.remove(
      socket_id
    )
