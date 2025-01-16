from dash import clientside_callback
from flask import request

from app import socketio, data_store
from reactivity import (
  out_storage_missing_data_counter,
  in_websocket,
  out_storage_background_task
)


@socketio.on("connect")
def handle_connect():
  data_store.connect(request.sid)
  print("Cliente conectado")


@socketio.on("disconnect")
def handle_disconnect():
  data_store.disconnect(request.sid)
  print("Cliente desconectado")


# Callback del lado del cliente para actualizar el contenido en tiempo real
clientside_callback(
  """
  ([background_task_status,missing_data_counter]) => {
      return [background_task_status,missing_data_counter];
  }
  """,
  [
    out_storage_background_task,
    out_storage_missing_data_counter
  ],
  in_websocket,
  prevent_initial_call=True
)

#
# @app_dash.callback(
#     Output("live-update-text", "children", allow_duplicate=True),
#     Input("start-button", "n_clicks"),
#     State("socketio", "socketId"),
#     prevent_initial_call=True
# )
# def start_updates(n_clicks, socket_id):
#     print(socket_id)
#     if n_clicks > 0 and socket_id:
#         socketio.start_background_task(generate_data)
#         return "Actualizaciones iniciadas..."
#     return "Presiona el botón para iniciar actualizaciones."


# def generate_data():
#     with app.app_context():
#         for i in range(10):
#             socketio.sleep(1)  # Cambia time.sleep por socketio.sleep
#             data = f"Actualización {i+1}"
#             for socket_id in clientes_conectados:
#                 socketio.emit("update", data, namespace="/", to=socket_id)
