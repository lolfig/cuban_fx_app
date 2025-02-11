from dash import callback

from layouts.layout_data_status.git_hub_component import out_slot_git_hub_days_counter
from components.github_cmp import generate_git_hub_days_counter_content
from reactivity.storage.missing_data_counter import in_storage_missing_data_counter


@callback(
  out_slot_git_hub_days_counter,
  in_storage_missing_data_counter,
  prevent_initial_call=False  # Forzamos
)
def update_git_hub_days_counter(missing_data_counter):
  return generate_git_hub_days_counter_content()
