import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify

stop_sync_btn = dbc.Button(
  children=[
    DashIconify(
      icon="mdi:stop",
      className="me-2",
      width=30,
    ),
    html.Span("Detener")
  ],
  title="Detener sincronización",
  className="flex-grow-1",
  n_clicks=0
)

layout = dbc.Row(
  class_name=["pb-3"],
  children=[
    dbc.Col([
      progressbar_sync_running := dbc.Progress(
        id="sync-progress",
        label='Sincronizando',
        animated=True,
        striped=True,
        value=0,
        max=100,
        color="success",
        style={"height": "100%"},
      )
    ],
      width=10,
    ),
    slot_fetch := dbc.Col(  # este slot es donde cambiaremos un botón por otro
      children=[(
        fetch_btn := dbc.Button([
          DashIconify(
            icon="mdi:sync",
            className="me-2",
            width=30,
          ),
          html.Span("Sincronizar")
        ],
          title="Sincronizar",
          className="flex-grow-1",
          n_clicks=0
        )
      )],
      className="d-flex flex-column",
      width=2
    )
  ])

from . import inputs, outputs
