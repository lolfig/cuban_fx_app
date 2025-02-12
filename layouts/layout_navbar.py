import dash_bootstrap_components as dbc
from dash import html, Output, Input
from dash_iconify import DashIconify

from config.const import MISSING_DATE_BADGE_COLOR, HIDDE

badge_indicator_missing_days = dbc.Badge(
  color=MISSING_DATE_BADGE_COLOR,
  pill=True,
  className=" ".join(
    [
      "position-absolute",
      "top-0",
      "end-0",
      "border",
      "border-light",
      "rounded-circle",
      "bg-danger",
      "p-2"
    ]),
  style={**HIDDE},
)
out_style_badge_indicator_missing_days = Output(badge_indicator_missing_days, "style")

drawer_menu_btn = dbc.Button(
  class_name='position-relative',
  title="Show Menu",
  n_clicks=0,
  children=[
    DashIconify(
      icon="mdi:menu",  # Ícono de Material Design
      width=30,
      height=30
    ),
    badge_indicator_missing_days,
  ],
)

in_click_drawer_menu_btn = Input(drawer_menu_btn, "n_clicks")

layout = dbc.Navbar(
  sticky="top",
  color="primary",
  children=dbc.Container([
    dbc.NavbarBrand(
      html.H3(
        'Cuban Currency Market Dashboard',
        className="--bs-light-text-emphasis text-light"
      ),
      href='/dash'
    ),
    drawer_menu_btn
  ]),
)
