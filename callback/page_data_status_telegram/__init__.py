from dash import callback, Output, Input, html, dcc, no_update
import dash_bootstrap_components as dbc
from config.settings import load_config
from config.telegram_status import get_all_channels_status

def _status_badge(status: str):
    color = {
        "ok": "success",
        "error": "danger",
        "unknown": "secondary"
    }.get(status, "secondary")
    return dbc.Badge(status.upper(), color=color, className="ms-2")

def _build_card(item: dict):
    return dbc.Card(
        dbc.CardBody([
            html.H5(item["channel"], className="card-title"),
            html.Div([
                html.Span("Estado: "),
                _status_badge(item["status"])
            ], className="mb-2"),
            html.Div([
                html.Small(f"Última corrida: {item['last_run'] or '—'}"),
            ], className="mb-1"),
            html.Div([
                html.Small(f"Nuevos mensajes: {item['new_messages']}"),
            ], className="mb-1"),
            html.Div([
                html.Small(f"Total mensajes: {item['total_messages']}"),
            ], className="mb-1"),
            html.Div([
                html.Small(f"Último error: {item['last_error'] or '—'}"),
            ], className="text-muted"),
        ])
    , className="mb-3")

@callback(
    Output("telegram-channel-cards", "children"),
    Input("url", "pathname"),
)
def render_telegram_cards(pathname: str):
    if not pathname or not pathname.startswith("/dash/telegram"):
        return no_update

    config = load_config()
    channels = config.get("channels", [])
    items = get_all_channels_status(channels)

    cols = [dbc.Col(_build_card(item), md=6, lg=4) for item in items] or [html.Div("No hay canales configurados.")]
    return dbc.Row(cols)