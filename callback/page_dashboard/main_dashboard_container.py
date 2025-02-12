import dash
from dash import callback

from layouts.page_dashboard import empty_space, fully_space
from layouts.page_dashboard.outputs import out_main_dashboard_container
from reactivity.storage.global_state import in_storage_global_state, state_storage_global_state
from data_storage import data_store




@callback(
  out_main_dashboard_container,
  in_storage_global_state,
  state_storage_global_state
)
def update_main_dashboard_container(global_state, last_global_state):
  if global_state == last_global_state:
    return dash.no_update
  if data_store.analytics is None:
    return empty_space
  return fully_space