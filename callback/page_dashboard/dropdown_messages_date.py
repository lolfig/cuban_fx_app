from dash import callback

from data_storage import data_store
from layouts.page_dashboard.outputs import out_pack_options_value_dropdown_messages_date
from reactivity import in_sync_trigger


@callback(
  out_pack_options_value_dropdown_messages_date,
  in_sync_trigger,
)
def update_dropdown_messages_date(n_clicks):
  if data_store.analytics is None or data_store.analytics.empty:
    return [], None
  
  return (
    elems := [date for date in data_store.analytics.index], elems[-1]
  )
