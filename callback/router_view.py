from dash import callback

from layouts import (
  layout_data_status,
  layout_dashboard
)
from reactivity import out_children_router_view, in_pathname_url


@callback(
  out_children_router_view,
  in_pathname_url
)
def display_page(pathname):
  if pathname == '/load_data':
    return layout_data_status.layout
  else:
    return layout_dashboard.layout
