import dash_bootstrap_components as dbc
from dash import html, Output, State
from dash_iconify import DashIconify
from config.const import MISSING_DATE_BADGE_COLOR

badge_missing_days = dbc.Badge(
  pill=True,
  color=MISSING_DATE_BADGE_COLOR,
)

out_pack_slot_style_badge_missing_days = [
  Output(badge_missing_days, "children"),
  Output(badge_missing_days, "style"),
]

navigation_drawer = dbc.Offcanvas(
  is_open=False,
  # backdrop="static",  # El drawer no se cierra al hacer clic fuera de él
  placement="start",  # Posición: 'start' para izquierda, 'end' para derecha
  children=[
    dbc.ListGroup([
      dbc.ListGroupItem(
        className="d-flex justify-content-between align-items-start",
        href="/dash",
        children=[
          html.Div(
            className="ms-2 me-auto",
            children="Home"
          )
        ]
      ),
      
      dbc.ListGroupItem(  # NUEVO
        className="d-flex justify-content-between align-items-start",
        href="/dash/social",
        children=[
          html.Div(
            className="ms-2 me-auto",
            children=[
              DashIconify(icon="mdi:account-group", className="me-2"),
              "Redes Sociales"
            ]
          )
        ]
      ),
      dbc.ListGroupItem(
        className="d-flex justify-content-between align-items-start",
        href="/dash/load_data",
        children=[
          html.Div(
            className="ms-2 me-auto",
            children="Datos Cargados"
          ),
          badge_missing_days
        ]
      ),
      
      dbc.ListGroupItem(
        className="d-flex justify-content-between align-items-start",
        href="/dash/telegram",
        children=[
          html.Div(
            className="ms-2 me-auto",
            children=[
              DashIconify(icon="mdi:telegram", className="me-2"),
              "Datos Cargados de Redes Sociales"
            ]
          )
        ]
      ),
      dbc.ListGroupItem(
        className="d-flex justify-content-between align-items-start",
        href="/dash/settings",
        children=[
          html.Div(
            className="ms-2 me-auto",
            children=[
              DashIconify(
                icon="mdi:cog",
                className="me-2",
                width=20
              ),
              "Configuración"
            ]
          )
        ]
      ),
      html.Div(style={'flex': '1'}),
      html.Form(
        action="/logout",
        method="post",
        children=[
          dbc.Button(
            "Logout",
            type="submit",
            color="danger",
            className="w-100 mt-3"
          )
        ],
        style={'padding': '1rem'}
      )
    ], style={'height': '100%', 'display': 'flex', 'flexDirection': 'column'}),
  ]
)

out_is_open_navigation_drawer = Output(navigation_drawer, "is_open", allow_duplicate=True)
state_is_open_navigation_drawer = State(navigation_drawer, "is_open")
