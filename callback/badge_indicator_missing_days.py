from dash import callback

from config.const import SHOW_INLINE_BLOCK, HIDDE
from layouts.layout_navbar import out_style_badge_indicator_missing_days
from reactivity.storage.missing_data_counter import in_storage_missing_data_counter


@callback(
  out_style_badge_indicator_missing_days,
  in_storage_missing_data_counter,
  prevent_initial_call=False  # Forzamos la ejecución en la primera carga
)
def update_badge(missing_data_counter):
  if missing_data_counter > 0:
    return SHOW_INLINE_BLOCK
  return HIDDE
