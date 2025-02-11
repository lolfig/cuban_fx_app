import dash
import dash_bootstrap_components as dbc
from dash import callback

import components as my_components
from layouts.layout_dashboard.outputs import out_slot_info_cards
from reactivity.storage.global_state import in_storage_global_state, state_storage_global_state
from store import data_store


@callback(
  out_slot_info_cards,
  in_storage_global_state,
  state_storage_global_state
)
def update_slot_info_cards(global_state, last_global_state):
  if global_state == last_global_state:
    return dash.no_update
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
