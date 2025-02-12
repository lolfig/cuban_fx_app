import dash_bootstrap_components as dbc
from dash import get_asset_url, dcc, html

import components as my_components
from app import data_store
from services import formaters

empty_space = dbc.Row(
  [
    dbc.Alert(
      color="warning",
      children=[
        html.H4("No hay datos descargados", className="alert-heading"),
        html.P(
          "Lo sentimos, pero no hay datos cargados en este momento. "
          "Por favor, ve a la pestaña de cargar datos para continuar. "
          "🙏 Gracias por tu comprensión."
        ),
        html.Hr(),
        html.A("Carga los datos aquí", href="/dash/load_data", className="alert-link"),
      ]
    )
  ]
)

fully_space = [
  slot_data_description := dbc.Row([]),
  my_components.head_lines.row_h3("Series Temporales"),
  slot_temporal_series := dbc.Row([]),
  my_components.head_lines.row_h3("Estadística Diaria"),
  dbc.Row([dbc.Col([(
    dropdown_date := dbc.Select(
      id="date-dropdown",
    
    )
  
  )], width=12
  )]),
  (statistics_graph_row := dbc.Row([
    dbc.Col(graph_histogram_vol_price := dcc.Graph(id="histogram-vol-price"), width=6),
    dbc.Col(graph_supply_demand := dcc.Graph(id="supply-demand"), width=6),
  ])),
  my_components.head_lines.row_h3("Mensajes"),
  slot_info_cards := dbc.Row([]),
  my_components.head_lines.row_h3("Procesado de Mensajes"),
  dbc.Row([
    dbc.Col(
      width=12,
      children=(
        dropdown_messages_date := dcc.Dropdown(id="messages-date-dropdown")
      )
    )
  ]),
  dbc.Row([
    dbc.Col(
      width=12,
      children=(
        slot_messages_table := html.Div(id="messages-table")
      ),
      style={
        "maxHeight": "300px",  # Ajusta esta altura según tus necesidades
        "overflowY": "auto",
      },
    )
  ]),
  my_components.head_lines.row_h3("Serie Temporal: Numero de Mensajes"),
  dbc.Row([
    number_messages := dbc.Col(
      width=12,
      children=[],
    )
  ]),
]

layout = dbc.Container([
  # logo row
  dbc.Row(
    className="my-3",
    children=[
      my_components.images.logo_image(
        src=get_asset_url("logo_clean.png"),
      ),
      my_components.images.logo_image(
        src=get_asset_url("ff_logo.png"),
      ),
    ],
  ),
  my_components.head_lines.row_h3("Información General"),
  main_dashboard_container := dbc.Container(
    children=[
      empty_space
    ]
  )
])

from . import inputs, outputs
