import dash_bootstrap_components as dbc
from dash import callback

import components as my_components
from data_storage import data_store
from layouts.page_dashboard.outputs import out_slot_info_cards
from reactivity import in_sync_trigger
from reactivity.storage.global_state import in_storage_global_state


@callback(
  out_slot_info_cards,
  in_sync_trigger
)
def update_slot_info_cards(n_clicks):
  if data_store.avg_daily_messages is None or data_store.percent_compra is None or data_store.percent_venta is None:
    return []
  
  return [
    dbc.Col(my_components.cards.basic_card(title, message), width=3)
    for title, message in [
      ("Mensajes con 4 campos", "94.41%"),
      ("Promedio Diario", f"{data_store.avg_daily_messages:.2f}"),
      ("Compra", f"{data_store.percent_compra:.2f}%"),
      ("Venta", f"{data_store.percent_venta:.2f}%"),
    ]
  ]
