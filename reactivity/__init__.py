from dash import dcc, html, Output, Input
from dash_socketio import DashSocketIO

websocket = DashSocketIO(
  id="socketio",
  eventNames=["update"],
)
in_websocket = Input(websocket, "data-update")

url = dcc.Location(id='url', refresh=False)
in_pathname_url = Input(url, 'pathname')
router_view = html.Div()
out_children_router_view = Output(router_view, 'children')
sync_trigger = html.Button(
  children="Sync",
  id="sync-trigger",
  style={"display": "none"}
)
in_sync_trigger = Input(sync_trigger, "n_clicks")

file_download = dcc.Download("download_component", data=None)
out_file_download = Output(file_download, "data")
