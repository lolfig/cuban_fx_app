import dash
from dash import callback

from data_storage import data_store
from layouts.page_dashboard.outputs import out_pack_options_value_dropdown_messages_date
from reactivity.storage.global_state import in_storage_global_state, state_storage_global_state


@callback(
  out_pack_options_value_dropdown_messages_date,
  in_storage_global_state,
  state_storage_global_state
)
def update_dropdown_messages_date(global_state, last_global_state):
  if global_state == last_global_state:
    return dash.no_update
  if data_store.analytics is None or data_store.analytics.empty:
    return [], None
  
  return (
    elems := [date for date in data_store.analytics.index.date], elems[-1]
  )
