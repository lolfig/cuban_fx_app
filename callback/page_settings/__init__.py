from dash import callback, Output, Input, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify
from config.settings import save_config, load_config

@callback(
    Output("channel-list", "children"),
    Input("add-channel-btn", "n_clicks"),
    State("channel-input", "value"),
    State("channel-list", "children"),
    prevent_initial_call=True
)
def update_channel_list(n_clicks, channel_url, existing_channels):
    if not channel_url:
        return existing_channels or []
    
    new_channel = dbc.ListGroupItem(
        [
            channel_url,
            dbc.Button(
                DashIconify(icon="mdi:delete", width=20),
                color="danger",
                size="sm",
                className="ms-2",
                id={"type": "delete-channel-btn", "index": n_clicks}
            )
        ],
        className="d-flex justify-content-between align-items-center"
    )
    
    if existing_channels:
        existing_channels.append(new_channel)
        return existing_channels
    return [new_channel]

@callback(
    Output("channel-list", "children", allow_duplicate=True),
    Input({"type": "delete-channel-btn", "index": ALL}, "n_clicks"),
    State("channel-list", "children"),
    prevent_initial_call=True
)
def delete_channel(n_clicks, existing_channels):
    if not any(n_clicks) or not existing_channels:
        return existing_channels
    
    # Encontrar qué botón fue clickeado
    triggered_id = ctx.triggered_id
    if triggered_id:
        index = triggered_id["index"]
        return [ch for i, ch in enumerate(existing_channels) if i != index]
    return existing_channels

@callback(
    [
        Output("save-settings-btn", "disabled"),
        Output("telegram-api-id", "value"),
        Output("telegram-api-hash", "value"),
        Output("telegram-phone", "value"),
        Output("telegram-username", "value"),
        Output("update-interval", "value"),
        Output("history-days", "value"),
        Output("settings-feedback", "children"),  # Nuevo output para el mensaje
        Output("settings-feedback", "is_open")    # Nuevo output para mostrar/ocultar el mensaje
    ],
    Input("save-settings-btn", "n_clicks"),
    State("telegram-api-id", "value"),
    State("telegram-api-hash", "value"),
    State("telegram-phone", "value"),
    State("telegram-username", "value"),
    State("channel-list", "children"),
    State("update-interval", "value"),
    State("history-days", "value"),
    prevent_initial_call=True
)
def save_settings(n_clicks, api_id, api_hash, phone, username, channels, update_interval, history_days):
    if not n_clicks:
        return False, api_id, api_hash, phone, username, update_interval, history_days, "", False
    
    # Validar campos requeridos
    if not all([api_id, api_hash, phone, username]):
        return False, api_id, api_hash, phone, username, update_interval, history_days, "❌ Todos los campos son requeridos", True
    
    channel_urls = []
    if channels:
        for channel in channels:
            channel_urls.append(channel["props"]["children"][0])
    
    config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone': phone,
        'username': username,
        'channels': channel_urls,
        'update_interval': update_interval,
        'history_days': history_days
    }
    
    save_config(config)
    return False, api_id, api_hash, phone, username, update_interval, history_days, "✅ Configuración guardada exitosamente", True

@callback(
    [
        Output("telegram-api-id", "value", allow_duplicate=True),
        Output("telegram-api-hash", "value", allow_duplicate=True),
        Output("telegram-phone", "value", allow_duplicate=True),
        Output("telegram-username", "value", allow_duplicate=True),
        Output("update-interval", "value", allow_duplicate=True),
        Output("history-days", "value", allow_duplicate=True),
        Output("channel-list", "children", allow_duplicate=True)
    ],
    Input("restore-settings-btn", "n_clicks"),
    prevent_initial_call="initial_duplicate"
)
def load_initial_values(n_clicks):
    config = load_config()
    
    # Initialize channel list
    channel_list = []
    if config.get('channels'):
        for i, channel in enumerate(config['channels']):
            channel_list.append(
                dbc.ListGroupItem(
                    [
                        channel,
                        dbc.Button(
                            DashIconify(icon="mdi:delete", width=20),
                            color="danger",
                            size="sm",
                            className="ms-2",
                            id={"type": "delete-channel-btn", "index": i}
                        )
                    ],
                    className="d-flex justify-content-between align-items-center"
                )
            )
    
    return [
        config.get('api_id', ''),
        config.get('api_hash', ''),
        config.get('phone', ''),
        config.get('username', ''),
        config.get('update_interval', 60),
        config.get('history_days', 30),
        channel_list
    ]
