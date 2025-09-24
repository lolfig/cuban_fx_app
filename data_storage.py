import asyncio
import datetime
import json
from os import path
from typing import Optional

from fastapi_socketio import SocketManager
from config.const import DIR_TELEGRAM_ANALYTICS, DIR_TELEGRAM_MESSAGES
from config.const import DIR_DATA_MESSAGES, DIR_DATA_ANALYTICS
from services.cache import (
    get_imfs,
    hidden_MM,
    load_data,
    generate_time_series,
    get_messages_metrics,
    get_time_serie_num_messages,
    prepare_daily_data,
)
from services.framework_analytics.data_analytics import DataAnalytics
from services.framework_scraping.data_processing import DataProcessing
from services.framework_scraping.time_series_fetcher import PriceTimeSeries
from services.framework_scraping.tools.missing_dates import get_missing_dates
import pandas as pd  # NUEVO


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
    print("dentro de sync_data")
    if len(missing_dates) > 0:
        fetcher = DataProcessing(dates=missing_dates, currency="USD")
        async for index, complete_date in async_enumerate(
            fetcher.do_process_messages()
        ):
            print(f"done {complete_date}")
            yield ((index + 1) / len(missing_dates)) * 100  # percent_completed


def recreate_analytics():
    # print("dentro de recreate_analytics")
    analytics = DataAnalytics.do_analytics(DIR_DATA_MESSAGES)
    # print("paso el do_analytics")
    analytics.dataframe.to_pickle(path.join(DIR_DATA_ANALYTICS, "analytics.pickle"))
    # print("paso el to_pickle")
    with open(path.join(DIR_DATA_ANALYTICS, "all_orders.json"), "w") as file:
        file.write(json.dumps(analytics.orders))


def recreate_telegram_analytics():
    """
    Genera y guarda el análisis de los mensajes de Telegram
    en un directorio separado para no confligir con El Toque.
    """
    analytics = DataAnalytics.do_analytics(DIR_TELEGRAM_MESSAGES)
    analytics.dataframe.to_pickle(path.join(DIR_TELEGRAM_ANALYTICS, "analytics.pickle"))
    with open(path.join(DIR_TELEGRAM_ANALYTICS, "all_orders.json"), "w") as file:
        file.write(json.dumps(analytics.orders))


class DataStorage:
    __reporter_dates = None

    def reload_from_file(self, recreate=False):
        # print("getting missing dates")
        self.__reporter_dates = get_missing_dates(DIR_DATA_MESSAGES)
        # print("paso el get_missing_dates")
        if recreate:
            # print("dentro del if")
            recreate_analytics()
        print("loading data")
        try:
            # print("dentro del try")
            self.analytics, PriceTimeSeries_obj = load_data(DIR_DATA_ANALYTICS)
            self.series = PriceTimeSeries_obj.toque_serie
            self.all_info = PriceTimeSeries_obj.toque_all_info
        except FileNotFoundError as e:
            # print("dentro del except")
            if len(self.processed_dates) > 0:
                recreate_analytics()
                self.analytics, PriceTimeSeries_obj = load_data(DIR_DATA_ANALYTICS)
                self.series = PriceTimeSeries_obj.toque_serie
                self.all_info = PriceTimeSeries_obj.toque_all_info

            else:
                print(
                    "no hay ficheros para cargar ... por favor sincronice o cargue los datos"
                )
                return
        self.price_series, self.volumes_series = generate_time_series(
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
        self.imfs = get_imfs(self.price_series)
        self.hmm = hidden_MM(self.all_info["Venta"], num_states=2, n_iter=50)
        # --- NUEVO: cargar analytics de Telegram ---
        self.reload_telegram_from_file()
        # --- NUEVO FIN ---

    def get_storage_update(self):
        return self.sync_progress, self.background_task, len(self.missing_dates)

    def __init__(self, socket_manager: Optional[SocketManager] = None):
        self.__background_task = False
        self.__sync_progress = 0
        self.websocket_clientes = set()
        self.socket_manager = socket_manager
        self.avg_daily_messages = None
        self.percent_compra = None
        self.percent_venta = None
        self.price_series = None
        self.volumes_series = None
        self.analytics = None
        self.series = None
        self.number_messages = None
        self.daily_data = None
        self.global_state = None
        self.all_info = None
        self.imfs = None
        self.hmm = None
        # --- NUEVO: propiedades de Telegram ---
        self.telegram_analytics = None
        self.telegram_number_messages = None
        self.telegram_daily_data = {}
        # --- NUEVO FIN ---
        self.reload_from_file()
        self.update_global_state()

    def update_global_state(self):
        self.global_state = str(datetime.datetime.now())

    @property
    def sync_progress(self):
        return self.__sync_progress

    @property
    def background_task(self) -> bool:
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
        if self.dates is None:
            return []

        return [day for (day, is_in) in self.dates if is_in == False]

    @property
    def processed_dates(self):
        return [day for (day, is_in) in self.dates if is_in == True]

    @property
    def dates(self):
        return self.__reporter_dates.dates

    async def update_status(self, *, update=None, socket_id=None):
        self.update_global_state()
        if update is not None:
            self.__sync_progress = update

        if self.socket_manager is None:
            return
        await self.socket_manager.emit(
            "update",
            [
                self.global_state,
            ],
            namespace="/",
            to=socket_id,
            # callback=lambda *args: print(args),
            # ignore_queue=True
        )
        await asyncio.sleep(1)
        print("-" * 30)
        print(
            "update: "
            + str(
                [
                    self.background_task,
                    len(self.missing_dates),
                    self.global_state,
                ]
            )
        )
        print("-" * 30)

    async def sync_data(self):
        print("sync data....")
        self.__reporter_dates = get_missing_dates(
            DIR_DATA_MESSAGES
        )  # super importante no quitar!!!
        print(f"Missing dates found: [{', '.join(self.missing_dates)}]")

        await self.update_background_task_status(True)
        try:
            await fetch_time_series(self.start_date, self.end_date)

            async for update in sync_data(self.missing_dates):
                self.__reporter_dates = get_missing_dates(
                    DIR_DATA_MESSAGES
                )  # super importante no quitar!!!
                await self.update_status(update=update)
                print("update: ", update)
            self.reload_from_file(recreate=True)
            await self.update_background_task_status(False)
        except Exception as exception:  # noqa
            self.reload_from_file(recreate=True)
            await self.update_background_task_status(False)

    def connect(self, socket_id):
        self.websocket_clientes.add(socket_id)

    def disconnect(self, socket_id):
        if socket_id in self.websocket_clientes:
            self.websocket_clientes.remove(socket_id)
    async def sync_telegram_data(self):
        """
        Ejecuta el scraping de Telegram para el rango configurado (history_days),
        guarda los parquet diarios en DIR_TELEGRAM_MESSAGES, recrea los analytics
        en DIR_TELEGRAM_ANALYTICS y recarga los datos en memoria.
        """
        try:
            from config.settings import load_config
            from services.framework_scraping.telegram_fetcher import fetch_telegram_messages

            cfg = load_config()
            history_days = cfg.get('history_days', 30)

            # Tomaremos como referencia 'hoy' en UTC y recorreremos hacia atrás
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            for i in range(history_days):
                # End: inicio del día (00:00:00) del día objetivo
                end_moment = now_utc.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=i)
                start_moment = end_moment - datetime.timedelta(days=1)

                # Ejecuta el scraper para ese rango y guarda parquet en messages_telegram
                await fetch_telegram_messages(
                    currency="USD",
                    start_moment=start_moment,
                    end_moment=end_moment
                )

            # Recalcular analytics de Telegram y recargarlos
            recreate_telegram_analytics()
            self.reload_telegram_from_file()

            # Notificar a clientes para refrescar UI
            await self.update_status()
        except Exception as e:
            print(f"Error en sync_telegram_data: {e}")
            raise

    def reload_telegram_from_file(self, recreate: bool = False):
        if recreate:
            try:
                recreate_telegram_analytics()
            except Exception as e:
                print(f"Error recreando analytics de Telegram: {e}")

        try:
            self.telegram_analytics = pd.read_pickle(
                path.join(DIR_TELEGRAM_ANALYTICS, "analytics.pickle")
            )
        except FileNotFoundError:
            self.telegram_analytics = None
            self.telegram_number_messages = None
            self.telegram_daily_data = {}
            return

        try:
            if self.telegram_analytics is not None and not self.telegram_analytics.empty:
                self.telegram_number_messages = get_time_serie_num_messages(self.telegram_analytics)
                self.telegram_daily_data = prepare_daily_data(self.telegram_analytics)
            else:
                self.telegram_number_messages = None
                self.telegram_daily_data = {}
        except Exception as e:
            print(f"Error preparando datos diarios de Telegram: {e}")
            self.telegram_number_messages = None
            self.telegram_daily_data = {}


data_store = DataStorage()


# --- NUEVO: método para recargar Telegram ---
