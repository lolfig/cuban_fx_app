import dash_bootstrap_components as dbc
from dash import dcc, html
from components import head_lines as custom_head_lines

# Definir los IDs para los nuevos componentes
tg_slot_info_cards = "tg-slot-info-cards"
tg_slot_hidden_markov_model = "tg-slot-hidden-markov-model"
tg_slot_empirical_mode_decomposition = "tg-slot-empirical-mode-decomposition"

layout = dbc.Container(
    [
        custom_head_lines.row_h1("Redes Sociales"),
        custom_head_lines.row_h3("Estadística Diaria"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Select(id="tg-date-dropdown"),
                    ],
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="tg-histogram-vol-price"), width=6),
                dbc.Col(dcc.Graph(id="tg-supply-demand"), width=6),
            ]
        ),
        custom_head_lines.row_h3("Mensajes"),
        dbc.Row(id=tg_slot_info_cards, children=[]),
        custom_head_lines.row_h3("Procesado de Mensajes"),
        dbc.Row(
            [
                dbc.Col(
                    width=12,
                    children=(dcc.Dropdown(id="tg-messages-date-dropdown")),
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    width=12,
                    children=(html.Div(id="tg-messages-table")),
                    style={"maxHeight": "300px", "overflowY": "auto"},
                )
            ]
        ),
        custom_head_lines.row_h3("Serie Temporal: Número de Mensajes"),
        dbc.Row([dbc.Col(width=12, children=(html.Div(id="tg-number-messages")))]),
        custom_head_lines.row_h3("Modelo Oculto de Markov"),
        dbc.Row(id=tg_slot_hidden_markov_model, children=[]),
        custom_head_lines.row_h3("Descomposición de Modos Empíricos"),
        dbc.Row(id=tg_slot_empirical_mode_decomposition, children=[]),
    ]
)