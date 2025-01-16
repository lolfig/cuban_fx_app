from dash import callback, no_update

from app import data_store, socketio
from layouts.layout_data_status import in_click_fetch_btn


@callback(
  in_click_fetch_btn,
  prevent_initial_call=True
)
def run_fetch(n_clicks):
  if n_clicks == 0:
    return no_update
  socketio.start_background_task(data_store.sync_data)
