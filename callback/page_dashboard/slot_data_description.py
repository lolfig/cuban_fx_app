from dash import callback

import components as my_components
from app import data_store
from layouts.page_dashboard.outputs import out_slot_data_description
from reactivity import in_sync_trigger
from reactivity.storage.global_state import in_storage_global_state


@callback(
  out_slot_data_description,
  in_sync_trigger
)
def update_slot_data_description(n_clicks):
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
