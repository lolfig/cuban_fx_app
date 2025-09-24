from dash import callback, Output, Input, State, MATCH, ALL, ctx
import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify
from config.settings import save_config, load_config

def make_channel_item(channel_url: str, btn_index=None):
    # Construye el item de lista con botón Eliminar
    # Usamos la URL como index del botón para que sea estable
    return dbc.ListGroupItem(
        [
            channel_url,
            dbc.Button(
                DashIconify(icon="mdi:delete", width=20),
                color="danger",
                outline=True,
                size="sm",
                className="ms-2",
                id={"type": "delete-channel-btn", "index": channel_url}
            )
        ],
        className="d-flex justify-content-between align-items-center"
    )

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
    
    # Sanea: quita espacios y backticks por si vinieran pegados
    channel_url = channel_url.strip().strip("`").strip()
    if not channel_url:
        return existing_channels or []
    
    # Evitar duplicados
    current = existing_channels or []
    current_urls = set()
    for ch in current:
        try:
            current_urls.add(ch["props"]["children"][0])
        except Exception:
            pass
    
    if channel_url in current_urls:
        return current  # ya existe
    
    new_channel = make_channel_item(channel_url)
    current.append(new_channel)
    return current

@callback(
    Output("channel-list", "children", allow_duplicate=True),
    Input({"type": "delete-channel-btn", "index": ALL}, "n_clicks"),
    State("channel-list", "children"),
    prevent_initial_call=True
)
def delete_channel(n_clicks, existing_channels):
    if not existing_channels or not any(n_clicks):
        return existing_channels
    
    # Identificar cuál botón disparó el evento
    triggered_id = ctx.triggered_id
    if not triggered_id:
        return existing_channels
    
    # triggered_id es un dict pattern-matching con la clave "index" (la URL del canal)
    channel_to_delete = triggered_id.get("index")
    if not channel_to_delete:
        return existing_channels
    
    # Filtra por URL, no por posición
    return [ch for ch in existing_channels if ch["props"]["children"][0] != channel_to_delete]

@callback(
    [
        Output("save-settings-btn", "disabled"),
        Output("telegram-api-id", "value"),
        Output("telegram-api-hash", "value"),
        Output("telegram-phone", "value"),
        Output("telegram-username", "value"),
        Output("update-interval", "value"),
        Output("history-days", "value"),
        Output("daily-run-time", "value"),
        Output("settings-feedback", "children"),
        Output("settings-feedback", "is_open")
    ],
    Input("save-settings-btn", "n_clicks"),
    State("telegram-api-id", "value"),
    State("telegram-api-hash", "value"),
    State("telegram-phone", "value"),
    State("telegram-username", "value"),
    State("channel-list", "children"),
    State("update-interval", "value"),
    State("history-days", "value"),
    State("daily-run-time", "value"),
    prevent_initial_call=True
)
def save_settings(n_clicks, api_id, api_hash, phone, username, channels, update_interval, history_days, daily_run_time):
    if not n_clicks:
        return False, api_id, api_hash, phone, username, update_interval, history_days, daily_run_time, "", False
    
    # Validar campos requeridos
    if not all([api_id, api_hash, phone, username]):
        return False, api_id, api_hash, phone, username, update_interval, history_days, daily_run_time, "❌ Todos los campos son requeridos", True
    
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
        'history_days': history_days,
        'daily_run_time': daily_run_time or ""  # string "HH:MM" o vacío
    }
    
    save_config(config)
    return False, api_id, api_hash, phone, username, update_interval, history_days, daily_run_time, "✅ Configuración guardada exitosamente", True

@callback(
    [
        Output("telegram-api-id", "value", allow_duplicate=True),
        Output("telegram-api-hash", "value", allow_duplicate=True),
        Output("telegram-phone", "value", allow_duplicate=True),
        Output("telegram-username", "value", allow_duplicate=True),
        Output("update-interval", "value", allow_duplicate=True),
        Output("history-days", "value", allow_duplicate=True),
        Output("daily-run-time", "value", allow_duplicate=True),
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
        for channel in config['channels']:
            channel_list.append(make_channel_item(channel))
    
    return [
        config.get('api_id', ''),
        config.get('api_hash', ''),
        config.get('phone', ''),
        config.get('username', ''),
        config.get('update_interval', 60),
        config.get('history_days', 30),
        config.get('daily_run_time', ''),  # "HH:MM" o ''
        channel_list
    ]

@callback(
    Output("run-telegram-scrape-status", "children"),
    Input("run-telegram-scrape-btn", "n_clicks"),
    prevent_initial_call=True
)
def run_telegram_scrape(n_clicks):
    if not n_clicks:
        return ""
    # Ejecutar scraping de Telegram (bloqueante mientras corre)
    try:
        import asyncio
        from data_storage import data_store
        asyncio.run(data_store.sync_telegram_data())
        return "✅ Scraping de Telegram completado. Revisa la página 'Redes Sociales'."
    except Exception as e:
        return f"❌ Error durante el scraping: {e}"
