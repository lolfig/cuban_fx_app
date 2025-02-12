from dash import callback

from data_storage import data_store
from layouts import (
  page_data_status,
  page_dashboard
)
from reactivity import out_children_router_view, in_pathname_url
from reactivity.storage.background_task import out_storage_background_task
from reactivity.storage.background_task_progress import out_storage_background_task_progress
from reactivity.storage.global_state import state_storage_global_state
from reactivity.storage.missing_data_counter import out_storage_missing_data_counter


@callback(
  [
    out_children_router_view,
    out_storage_background_task_progress,
    out_storage_background_task,
    out_storage_missing_data_counter
  ],
  in_pathname_url,
  state_storage_global_state,
  prevent_initial_call=True
)
def display_page(pathname, global_state):
  print("-" * 20)
  print(f"entre a la pagina con el estate {data_store.global_state}")
  print("-" * 20)
  
  data = data_store.get_storage_update()
  
  if pathname == '/dash/load_data':
    return page_data_status.layout, *data
  else:
    return page_dashboard.layout, *data
