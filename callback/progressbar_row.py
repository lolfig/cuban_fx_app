from dash import callback

from layouts.layout_data_status.progressbar_row.outputs import out_value_progressbar__sync_running
from reactivity.storage.background_task_progress import in_storage_background_task_progress
from reactivity.storage.background_task import in_storage_background_task


@callback(
  out_value_progressbar__sync_running,
  in_storage_background_task,
  in_storage_background_task_progress,
  prevent_initial_call=True  # Forzamos
)
def update_progressbar_row(storage_background_task: bool, storage_background_task_progress: int):
  if storage_background_task:
    return storage_background_task_progress
  return 0
