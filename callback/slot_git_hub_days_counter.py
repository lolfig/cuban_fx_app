from dash import callback

from layouts.layout_data_status import (
  out_slot_git_hub_days_counter,
  generate_git_hub_days_counter_content
)
from reactivity import in_storage_missing_data_counter


@callback(
  out_slot_git_hub_days_counter,
  in_storage_missing_data_counter,
  prevent_initial_call=False  # Forzamos
)
def update_git_hub_days_counter(missing_data_counter):
  print("update_git_hub_days_counter")
  return generate_git_hub_days_counter_content()
