from dash import callback

from data_storage import data_store
from layouts.page_dashboard import empty_space, fully_space
from layouts.page_dashboard.outputs import out_main_dashboard_container
from reactivity import in_sync_trigger
from reactivity.storage.global_state import in_storage_global_state


@callback(
  out_main_dashboard_container,
  in_sync_trigger
)
def update_main_dashboard_container(n_clicks):
  if data_store.analytics is None:
    return empty_space
  return fully_space
