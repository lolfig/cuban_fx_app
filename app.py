import dash
from dash import html
from dash_bootstrap_components import themes as bootstrap_themes
from fastapi import FastAPI
from fastapi_socketio import SocketManager
from starlette.middleware.wsgi import WSGIMiddleware

app = FastAPI()
socket_manager = SocketManager(
  app=app,
  mount_location="/socket.io",  # este valor es obligatorio por dash_websocket.io
)

from data_storage import data_store

data_store.socket_manager = socket_manager

# dash app!!!
dash_app = dash.Dash(
  __name__,
  requests_pathname_prefix="/dash/",
  suppress_callback_exceptions=True,
  external_stylesheets=[
    bootstrap_themes.BOOTSTRAP
  ]
)

from reactivity import (
  url,
  storage,
  websocket,
  router_view,
  file_download, sync_trigger,

)

from layouts import (
  layout_navbar,
  layout_drawer
)

dash_app.layout = html.Div([
  url,
  websocket,
  sync_trigger, # este es el trigger para sincronizar los datos
  storage.storage_missing_data_counter,
  storage.storage_background_task_progress,
  storage.storage_background_task,
  storage.storage_global_state,
  layout_navbar.layout,
  layout_drawer.navigation_drawer,
  router_view,
  file_download,
])

import callback  # noqa


# Now mount you dash server into main fastapi application
@socket_manager.on("connect")
def handle_connect(sid, *args):
  data_store.connect(sid)
  print("Cliente conectado")


@socket_manager.on("disconnect")
def handle_disconnect(sid, *args):
  data_store.disconnect(sid)
  print("Cliente desconectado")


app.mount("/dash", WSGIMiddleware(dash_app.server))
import routes # noqa
