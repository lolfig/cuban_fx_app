import dash_bootstrap_components as dbc
from dash import get_asset_url, dcc, html, Output, Input
from plotly import express as px

import components as my_components
from app import data_store
from services import formaters

logo_row = dbc.Row(
  className="my-3",
  children=[
    my_components.images.logo_image(
      src=get_asset_url("logo_clean.png"),
    ),
    my_components.images.logo_image(
      src=get_asset_url("ff_logo.png"),
    ),
  ],
)
data_description = dbc.Row([
  my_components.tables.table_head(
    "Inicio de la Serie",
    data_store.price_series[["USDCUP_Marginal"]]
    .reset_index()
    .rename(columns={"index": "fecha"})
    .head(8),
  ),
  my_components.tables.table_head(
    "Final de la Serie",
    data_store.price_series[["USDCUP_Marginal"]]
    .reset_index()
    .rename(columns={"index": "fecha"})
    .tail(8),
  ),
  my_components.tables.table_head(
    "Métricas",
    data_store.price_series[["USDCUP_Marginal"]]
    .describe()
    .reset_index()
    .rename(columns={"index": "estadística"}),
  ),
])
statistics_graph_row = dbc.Row([
  dbc.Col(graph_histogram_vol_price := dcc.Graph(id="histogram-vol-price"), width=6),
  dbc.Col(graph_supply_demand := dcc.Graph(id="supply-demand"), width=6),
])

out_pack_figure_graphs = [
  Output(graph_histogram_vol_price, "figure"),
  Output(graph_supply_demand, "figure")
]

dropdown_date = dbc.Select(
  id="date-dropdown",
  options=(
    elems := [
      formaters.datetime_to_str(date)
      for date in data_store.analytics.index.unique()
    ]
  ),
  value=elems[-1],
)

in_value_dropdown_date = Input(dropdown_date, "value")
slot_messages_table = html.Div(id="messages-table")
out_slot_messages_table = Output(slot_messages_table, "children")

dropdown_messages_date = dcc.Dropdown(
  id="messages-date-dropdown",
  options=(
    elems := [date for date in data_store.analytics.index.date]
  ), value=elems[-1],
)

in_value_dropdown_messages_date = Input(dropdown_messages_date, "value")

layout = dbc.Container([
  logo_row,
  my_components.head_lines.row_h3("Información General"),
  data_description,
  my_components.head_lines.row_h3("Series Temporales"),
  dbc.Row([
    dbc.Col(
      dcc.Graph(
        figure=px.line(
          data_store.price_series.round(2),
          title="Serie de Precios"
        )
      ), width=12,
    ),
  ]),
  dbc.Row([
    dbc.Col(
      dcc.Graph(
        figure=px.line(
          data_store.volumes_series.round(2),
          title="Serie de Volúmenes",
        )
      ), width=12,
    )
  ]
  ),
  my_components.head_lines.row_h3("Estadística Diaria"),
  dbc.Row([dbc.Col([dropdown_date], width=12, )]),
  statistics_graph_row,
  my_components.head_lines.row_h3("Mensajes"),
  dbc.Row([
    dbc.Col(my_components.cards.basic_card(title, message), width=3)
    for title, message in [
      ("Mensajes con 4 campos", "94.41%"),
      ("Promedio Diario", f"{data_store.avg_daily_messages:.2f}"),
      ("Compra", f"{data_store.percent_compra:.2f}%"),
      ("Venta", f"{data_store.percent_venta:.2f}%"),
    ]
  ]),
  my_components.head_lines.row_h3("Procesado de Mensajes"),
  dbc.Row([
    dbc.Col(
      width=12,
      children=dropdown_messages_date
    )
  ]),
  dbc.Row([
    dbc.Col(
      width=12,
      children=slot_messages_table,
      style={
        "maxHeight": "300px",  # Ajusta esta altura según tus necesidades
        "overflowY": "auto",
      },
    )
  ]),
  my_components.head_lines.row_h3("Serie Temporal: Numero de Mensajes"),
  dbc.Row([
    dbc.Col(
      width=12,
      children=dcc.Graph(
        figure=px.line(
          data_store.number_messages.round(2),
        )
      ),
    )
  ]),
])
