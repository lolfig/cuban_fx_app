from dash import callback

from layouts.layout_data_status.progressbar_row import fetch_btn, stop_sync_btn
from layouts.layout_data_status.progressbar_row.outputs import out_slot_slot_fetch
from reactivity.storage.background_task import in_storage_background_task


@callback(
  out_slot_slot_fetch,
  in_storage_background_task
)
def update_slot_fetch(storage_background_task: bool):
  if storage_background_task:
    return stop_sync_btn
  return fetch_btn
