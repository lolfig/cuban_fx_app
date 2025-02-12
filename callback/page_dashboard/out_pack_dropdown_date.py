from dash import callback

from data_storage import data_store
from layouts.page_dashboard.outputs import out_pack_dropdown_date
from reactivity import in_sync_trigger
from services import formaters


@callback(
  out_pack_dropdown_date,
  in_sync_trigger
)
def update_pack_dropdown_date(n_click):
  # out_pack_dropdown_date = [
  #   out_value_dropdown_date,
  #   out_options_dropdown_date,
  #   out_disabled_dropdown_date
  # ]
  return (
    elems := [
      formaters.datetime_to_str(date)
      for date in data_store.processed_dates
    ],
    elems[-1] if len(elems) > 0 else None,
    len(elems) == 0
  )
