from dash import Input

from . import fetch_btn, stop_sync_btn

in_click_fetch_btn = Input(
  fetch_btn,
  "n_clicks"
)
in_stop_sync_btn = Input(
  stop_sync_btn,
  "n_clicks"
)
