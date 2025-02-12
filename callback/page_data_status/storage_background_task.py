from dash import callback, no_update, State

from layouts.page_data_status.progressbar_row.inputs import in_click_fetch_btn, in_stop_sync_btn
from reactivity.storage.background_task import storage_background_task, out_storage_background_task, \
  state_storage_background_task
from tasks.sync_manager import sync_manager


@callback(
  out_storage_background_task,
  in_stop_sync_btn,
  state_storage_background_task,
  prevent_initial_call=True
)
def run_stop_data_sync(n_clicks, is_running):
  if n_clicks == 0 or not is_running:
    return no_update
  
  sync_manager.stop_sync_data()
  return False


@callback(
  out_storage_background_task,
  in_click_fetch_btn,
  state_storage_background_task,
  prevent_initial_call=True
)
def run_data_sync(n_clicks, is_running):
  if n_clicks == 0 or is_running:
    return no_update
  
  sync_manager.run_sync_data()
  return True
