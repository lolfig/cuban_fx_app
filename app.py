import dash
from dash import html
from dash_bootstrap_components import themes as bootstrap_themes
from flask import Flask
from flask_socketio import SocketIO

import callback
from store import DataStore

server = Flask(__name__)
socketio = SocketIO(server, async_mode="eventlet")

data_store = DataStore(socketio)

# dash app!!!
dash_app = dash.Dash(
  __name__,
  suppress_callback_exceptions=True,
  server=server,
  external_stylesheets=[
    bootstrap_themes.BOOTSTRAP
  ],
)

from reactivity import (
  storage_missing_data_counter,
  storage_background_task,
  websocket,
  router_view,
  url,
  file_download,
)

from layouts import (
  layout_navbar,
  layout_drawer
)

dash_app.layout = html.Div([
  url,
  websocket,
  storage_missing_data_counter,
  storage_background_task,
  layout_navbar.layout,
  layout_drawer.navigation_drawer,
  router_view,
  file_download,
])

callback.register_callbacks()
