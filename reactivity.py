from dash import dcc, html, Output, Input
from dash.dcc import Store
from dash_socketio import DashSocketIO

from app import data_store

storage_missing_data_counter = Store(
  id='missing_data_counter_storage',
  data=len(data_store.missing_dates)
)
out_storage_missing_data_counter = Output(
  storage_missing_data_counter,
  "data"
)
in_storage_missing_data_counter = Input(
  storage_missing_data_counter,
  "data"
)

storage_background_task = Store(
  id='storage_background_task',
  data=len(data_store.missing_dates)
)

out_storage_background_task = Output(
  storage_background_task,
  'data'
)

in_storage_background_task = Input(
  storage_background_task,
  "data"
)

websocket = DashSocketIO(id="socketio", eventNames=["update"])
in_websocket = Input(websocket, "data-update")

url = dcc.Location(id='url', refresh=False)
in_pathname_url = Input(url, 'pathname')
router_view = html.Div()
out_children_router_view = Output(router_view, 'children')

file_download = dcc.Download("download_component", data=None)
out_file_download = Output(file_download, "data")
