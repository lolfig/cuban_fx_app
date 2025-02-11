import dash
from dash import callback

import components as my_components
from app import data_store
from layouts.layout_dashboard.outputs import out_slot_data_description
from reactivity.storage.global_state import in_storage_global_state, state_storage_global_state


@callback(
  out_slot_data_description,
  in_storage_global_state,
  state_storage_global_state
)
def update_slot_data_description(global_state, last_global_state):
  if global_state == last_global_state:
    return dash.no_update
  if data_store.price_series is None or data_store.price_series.empty:
    return []
  
  USDCUP_marginal_ = data_store.price_series[["USDCUP_Marginal"]].reset_index()  # noqa N806
  return [my_components.tables.table_head(
    "Inicio de la Serie",
    USDCUP_marginal_
    .rename(columns={"index": "fecha"})
    .head(8),
  ),
    my_components.tables.table_head(
      "Final de la Serie",
      USDCUP_marginal_
      .rename(columns={"index": "fecha"})
      .tail(8),
    ),
    my_components.tables.table_head(
      "Métricas",
      USDCUP_marginal_
      .describe()
      .reset_index()
      .rename(columns={"index": "estadística"}),
    ),
  ]
