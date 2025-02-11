import dash
from dash import html
from flask import Flask
from flask_socketio import SocketIO, emit

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
socketio = SocketIO(server)


@app.layout
def layout():
  return html.Div([
    html.Button("Ejecutar WebSocket", id="ws-btn"),
    html.Div(id="ws-status"),
  ])


@socketio.on('connect')
def handle_connect():
  emit('response', {'status': 'Conectado al servidor.'})


@socketio.on('update')
def handle_update(data):
  emit('response', {'message': f"Datos recibidos: {data}"}, broadcast=True)


if __name__ == "__main__":
  socketio.run(server, debug=True)
