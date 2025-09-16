import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_iconify import DashIconify
from components import head_lines as custom_head_lines
# ... existing code ...

# Página "Datos Cargados de Telegram"
layout = dbc.Container([
    custom_head_lines.row_h1("Datos Cargados de Telegram"),

    # Contenedor donde se renderizan las tarjetas de estado de canales
    dbc.Row([
        dbc.Col(
            html.Div(id="telegram-channel-cards", className="mt-3"),
            width=12
        )
    ]),
])
# ... existing code ...