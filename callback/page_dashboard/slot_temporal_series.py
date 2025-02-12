import dash_bootstrap_components as dbc
from dash import callback, dcc
from plotly import express as px

from data_storage import data_store
from layouts.page_dashboard.outputs import out_slot_temporal_series
from reactivity import in_sync_trigger


@callback(
  out_slot_temporal_series,
  in_sync_trigger
)
def update_slot_temporal_series(n_clicks):
  if data_store.price_series is None or data_store.volumes_series is None:
    return []
  
  return [
    dbc.Col(
      dcc.Graph(
        figure=px.line(
          data_store.price_series.round(2),
          title="Serie de Precios"
        )
      ), width=12,
    ),
    dbc.Col(
      dcc.Graph(
        figure=px.line(
          data_store.volumes_series.round(2),
          title="Serie de Volúmenes",
        )
      ), width=12,
    )
  ]
