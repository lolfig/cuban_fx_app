from dash import callback

from layouts.layout_data_status import out_slot_slot_fetch, fetching_btn, fetch_btn
from reactivity import in_storage_background_task


@callback(
  out_slot_slot_fetch,
  in_storage_background_task
)
def update_slot_fetch(storage_background_task: bool):
  if storage_background_task:
    return fetching_btn
  return fetch_btn
