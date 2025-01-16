from dash import callback

from layouts.layout_drawer import out_is_open_navigation_drawer, state_is_open_navigation_drawer
from layouts.layout_navbar import in_click_drawer_menu_btn


@callback(
  out_is_open_navigation_drawer,
  in_click_drawer_menu_btn,
  state_is_open_navigation_drawer,
  prevent_initial_call=True
)
def toggle_drawer(n1, is_open):
  if n1:
    return not is_open
  return is_open
