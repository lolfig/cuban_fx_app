from dash import callback

from layouts.page_data_status.progressbar_row.outputs import out_pack_progressbar__sync_running
from reactivity.storage.background_task import in_storage_background_task
from reactivity.storage.background_task_progress import in_storage_background_task_progress


@callback(
  out_pack_progressbar__sync_running,
  in_storage_background_task,
  in_storage_background_task_progress,
  prevent_initial_call=True  # Forzamos
)
def update_progressbar_row(storage_background_task: bool, storage_background_task_progress: int):
  # out_pack_progressbar__sync_running = [
  #   out_value_progressbar__sync_running,
  #   out_label_progressbar__sync_running,
  #   out_animated_progressbar__sync_running,
  #   out_color_progressbar__sync_running
  # ]
  value = max(storage_background_task_progress, 30)
  label = "Sincronizando" if storage_background_task else "Detenido"
  animated = storage_background_task
  color = "success" if storage_background_task else "danger"
  return value, label, animated, color
