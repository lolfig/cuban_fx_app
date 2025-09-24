from dash import callback, Output, Input, no_update, dcc, html
from plotly import graph_objects as go
from plotly import express as px

from data_storage import data_store
from reactivity import in_sync_trigger
from services.cache import load_raw_messages_telegram

# Importar los nuevos callbacks
from .slot_info_cards import update_tg_slot_info_cards
from .slot_hidden_markov_model import update_tg_slot_hidden_markov_model
from .slot_empirical_mode_decomposition import update_tg_slot_empirical_mode_decomposition

@callback(
    Output("tg-date-dropdown", "options"),
    Output("tg-date-dropdown", "value"),
    in_sync_trigger,
)
def tg_update_date_dropdown(_):
    analytics = data_store.telegram_analytics
    if analytics is None or analytics.empty:
        return [], None
    # Fix: Check if index items are datetime objects before calling strftime
    opts = []
    for d in analytics.index:
        if hasattr(d, 'strftime'):
            opts.append(d.strftime("%Y-%m-%d"))
        else:
            # If it's already a string, use it directly
            opts.append(str(d))
    return opts, opts[-1] if opts else None

@callback(
    Output("tg-histogram-vol-price", "figure"),
    Output("tg-supply-demand", "figure"),
    Input("tg-date-dropdown", "value"),
)
def tg_update_daily_histograms(selected_date):
    if not selected_date:
        return {}, {}
    daily = data_store.telegram_daily_data or {}
    if selected_date not in daily:
        return {}, {}

    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=daily[selected_date]["Compras_ordenadas"].index,
            y=daily[selected_date]["Compras_ordenadas"].values,
            mode="lines+markers",
            name="Demanda (Compra)",
            line=dict(color="blue"),
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=daily[selected_date]["Ventas_ordenadas"].index,
            y=daily[selected_date]["Ventas_ordenadas"].values,
            mode="lines+markers",
            name="Oferta (Venta)",
            line=dict(color="red"),
        )
    )
    fig1.update_layout(
        title="Histograma Volumen-Precio",
        xaxis_title="Precio",
        yaxis_title="Volumen (USD)",
    )

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=daily[selected_date]["Nivel_volumen_compra"],
            y=daily[selected_date]["Nivel_precio_compra"],
            mode="lines",
            name="Demanda (Compras)",
            line=dict(color="blue"),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=daily[selected_date]["Nivel_volumen_venta"],
            y=daily[selected_date]["Nivel_precio_venta"],
            mode="lines",
            name="Oferta (Ventas)",
            line=dict(color="red"),
        )
    )
    fig2.update_layout(
        title="Oferta y Demanda",
        xaxis_title="Cantidad de Volumen en USD",
        yaxis_title="Precio en CUP",
    )

    return fig1, fig2

@callback(
    Output("tg-messages-date-dropdown", "options"),
    Output("tg-messages-date-dropdown", "value"),
    in_sync_trigger,
)
def tg_update_messages_date_dropdown(_):
    analytics = data_store.telegram_analytics
    if analytics is None or analytics.empty:
        return [], None
    # Fix: Check if index items are datetime objects before calling strftime
    opts = []
    for d in analytics.index:
        if hasattr(d, 'strftime'):
            opts.append(d.strftime("%Y-%m-%d"))
        else:
            # If it's already a string, use it directly
            opts.append(str(d))
    return opts, opts[-1] if opts else None

@callback(
    Output("tg-messages-table", "children"),
    Input("tg-messages-date-dropdown", "value"),
)
def tg_update_messages_table(selected_date):
    if not selected_date:
        return html.P("No hay mensajes para mostrar")
    mess = load_raw_messages_telegram(selected_date)
    if not mess.empty:
        return dcc.Graph(figure=px.imshow(mess)) if False else \
            html.Div(children=[html.Div(mess.to_html(index=False), className="table-responsive")])
    return html.P("No hay mensajes para mostrar")

@callback(
    Output("tg-number-messages", "children"),
    in_sync_trigger,
)
def tg_update_number_messages(_):
    df = data_store.telegram_number_messages
    if df is None or df.empty:
        return None
    return dcc.Graph(figure=px.line(df.round(2), title="Número de mensajes"))