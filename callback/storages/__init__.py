from dash import callback

from data_storage import data_store
from reactivity import in_sync_trigger
from reactivity.storage.background_task import out_storage_background_task
from reactivity.storage.background_task_progress import out_storage_background_task_progress
from reactivity.storage.missing_data_counter import out_storage_missing_data_counter


@callback(
  [
    out_storage_background_task_progress,
    out_storage_background_task,
    out_storage_missing_data_counter
  ],
  in_sync_trigger,
  prevent_initial_call=True
)
def update_client_storages(n_clicks):
  return data_store.get_storage_update()
