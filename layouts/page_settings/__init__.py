import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_iconify import DashIconify
from components import head_lines as custom_head_lines

layout = dbc.Container([
    custom_head_lines.row_h1("Configuración del Sistema"),
    
    # Sección de Configuración de Telegram
    dbc.Card(
        dbc.CardBody([
            html.H4([
                DashIconify(icon="mdi:telegram", className="me-2"),
                "Configuración de Telegram"
            ]),
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("API ID"),
                        dbc.Input(type="text", id="telegram-api-id", placeholder="Ingrese su API ID", required=True),
                        dbc.FormFeedback("Este campo es requerido", type="invalid")
                    ], width=6),
                    dbc.Col([
                        dbc.Label("API Hash"),
                        dbc.Input(type="password", id="telegram-api-hash", placeholder="Ingrese su API Hash", required=True),
                        dbc.FormFeedback("Este campo es requerido", type="invalid")
                    ], width=6)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Número de Teléfono"),
                        dbc.Input(type="text", id="telegram-phone", placeholder="+1234567890", required=True),
                        dbc.FormFeedback("Este campo es requerido", type="invalid")
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Username"),
                        dbc.Input(type="text", id="telegram-username", placeholder="@username", required=True),
                        dbc.FormFeedback("Este campo es requerido", type="invalid")
                    ], width=6)
                ], className="mt-3")
            ])
        ]),
        className="mb-3"
    ),
    
    # Sección de Configuración de Canales
    dbc.Card(
        dbc.CardBody([
            html.H4([
                DashIconify(icon="mdi:channels", className="me-2"),
                "Canales de Telegram"
            ]),
            dbc.InputGroup([
                dbc.Input(id="channel-input", placeholder="https://t.me/nombre_canal"),
                dbc.Button("Agregar", id="add-channel-btn", color="primary")
            ], className="mb-3"),
            html.Div(id="channel-list")
        ]),
        className="mb-3"
    ),
    
    # Sección de Configuración de Análisis
    dbc.Card(
        dbc.CardBody([
            html.H4([
                DashIconify(icon="mdi:chart-line", className="me-2"),
                "Configuración de Análisis"
            ]),
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Intervalo de Actualización (minutos)"),
                        dbc.Input(type="number", id="update-interval", value=5, min=1)
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Días de Histórico"),
                        dbc.Input(type="number", id="history-days", value=30, min=1)
                    ], width=6)
                ])
            ])
        ])
    ),
    
    # Botones de Acción
    dbc.Row([
        dbc.Col([
            dbc.Button("Guardar Cambios", id="save-settings-btn", color="primary", className="me-2"),
            dbc.Button(
                ["Restaurar Valores", DashIconify(icon="mdi:restore", className="ms-2")],
                id="restore-settings-btn",
                color="warning"
            )
        ], className="d-flex justify-content-end mt-3")
    ]),
    
    # Mensaje de confirmación en una fila separada
    dbc.Row([
        dbc.Col([
            dbc.Alert(
                id="settings-feedback",
                is_open=False,
                duration=4000,
                dismissable=True,
                color="success",
                className="mt-3 mb-0 d-flex align-items-center",
                style={"maxWidth": "400px", "margin": "0 auto"}
            )
        ], className="d-flex justify-content-center")
    ])
])