from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from app_dashboard.cmp.my_card import my_card
from tools import formaters
from .tools import cache as tools_cache
from tools.const import DIR_DATA_ANALYTICS
import dash_bootstrap_components as dbc


# Initialize the Dash app
def load_dashboard(app):

    # Load data
    analytics, series = tools_cache.load_data(DIR_DATA_ANALYTICS)
    price_series, volumes_series = tools_cache.load_time_series(analytics, series)
    (
        avg_daily_messages,
        _,
        _,
        percent_compra,
        percent_venta,
    ) = tools_cache.get_messages_metrics(analytics)
    number_messages = tools_cache.get_time_serie_num_messages(analytics)
    daily_data = tools_cache.prepare_daily_data(analytics)

    app.layout = html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url("ff_logo.png"),
                                    style={
                                        "display": "block",
                                        "margin": "0 auto",
                                        "width": "150px",
                                    },
                                ),
                                className="mb-2",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Cuban Currency Market Dashboard",
                                    className="text-center",
                                ),
                                className="mb-4 mt-2",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3("Información Básica (USD/CUP)"),
                                className="mb-4",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H4("Inicio de la Serie"),
                                    dbc.Table.from_dataframe(
                                        price_series[["USDCUP_Marginal"]]
                                        .head(8)
                                        .reset_index(),
                                        striped=True,
                                        bordered=True,
                                        hover=True,
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    html.H4("Final de la Serie"),
                                    dbc.Table.from_dataframe(
                                        price_series[["USDCUP_Marginal"]]
                                        .tail(8)
                                        .reset_index(),
                                        striped=True,
                                        bordered=True,
                                        hover=True,
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    html.H4("Métricas"),
                                    dbc.Table.from_dataframe(
                                        price_series[["USDCUP_Marginal"]]
                                        .describe()
                                        .reset_index(),
                                        striped=True,
                                        bordered=True,
                                        hover=True,
                                    ),
                                ],
                                width=4,
                            ),
                        ]
                    ),
                    dbc.Row([dbc.Col(html.H3("Series Temporales"), className="mb-4")]),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=px.line(
                                        price_series, title="Serie de Precios"
                                    )
                                ),
                                width=12,
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=px.line(
                                        volumes_series, title="Serie de Volúmenes"
                                    )
                                ),
                                width=12,
                            )
                        ]
                    ),
                    dbc.Row([dbc.Col(html.H3("Estadística Diaria"), className="mb-4")]),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    id="date-dropdown",
                                    options=(
                                        elems := [
                                            formaters.date_format(date)
                                            for date in analytics.index.unique()
                                        ]
                                    ),
                                    value=elems[-1],
                                ),
                                width=12,
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id="histogram-vol-price"), width=6),
                            dbc.Col(dcc.Graph(id="supply-demand"), width=6),
                        ]
                    ),
                    dbc.Row([dbc.Col(html.H3("Mensajes"), className="mb-4")]),
                    dbc.Row(
                        [
                            dbc.Col(my_card(title, message), width=3)
                            for title, message in [
                                ("% Mensajes con 4 campos", "94.41%"),
                                ("Promedio Diario", f"{avg_daily_messages}"),
                                ("% Compra", f"{percent_compra}%"),
                                ("% Venta", f"{percent_venta}%"),
                            ]
                        ]
                    ),
                    dbc.Row(
                        [dbc.Col(html.H3("Procesado de Mensajes"), className="mb-4")]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    id="messages-date-dropdown",
                                    options=(
                                        elems := [date for date in analytics.index.date]
                                    ),
                                    value=elems[-1],
                                ),
                                width=12,
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(id="messages-table"),
                                width=12,
                                style={
                                    "maxHeight": "300px",  # Ajusta esta altura según tus necesidades
                                    "overflowY": "auto",
                                },
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H3("Serie Temporal: Numero de Mensajes"),
                                className="mb-4",
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=px.line(
                                        number_messages,
                                        title="Serie Temporal: Numero de Mensajes",
                                    )
                                ),
                                width=12,
                            )
                        ]
                    ),
                ]
            )
        ]
    )

    @app.callback(
        Output("histogram-vol-price", "figure"),
        Output("supply-demand", "figure"),
        Input("date-dropdown", "value"),
    )
    def update_daily_histograms(selected_date):
        selected_date = formaters.from_string(selected_date)
        if selected_date and (selected_date in daily_data):
            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=daily_data[selected_date]["Compras_ordenadas"].index,
                    y=daily_data[selected_date]["Compras_ordenadas"].values,
                    mode="lines+markers",
                    name="Demanda (Compra)",
                    line=dict(color="blue"),
                )
            )
            fig1.add_trace(
                go.Scatter(
                    x=daily_data[selected_date]["Ventas_ordenadas"].index,
                    y=daily_data[selected_date]["Ventas_ordenadas"].values,
                    mode="lines+markers",
                    name="Oferta (Venta)",
                    line=dict(color="red"),
                )
            )
            fig1.update_layout(
                title="Histograma Volúmen-Precio",
                xaxis_title="Precio",
                yaxis_title="Volumen (USD)",
            )

            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=daily_data[selected_date]["Nivel_volumen_compra"],
                    y=daily_data[selected_date]["Nivel_precio_compra"],
                    mode="lines",
                    name="Demanda (Compras)",
                    line=dict(color="blue"),
                )
            )
            fig2.add_trace(
                go.Scatter(
                    x=daily_data[selected_date]["Nivel_volumen_venta"],
                    y=daily_data[selected_date]["Nivel_precio_venta"],
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
        return {}, {}

    @app.callback(
        Output("messages-table", "children"), Input("messages-date-dropdown", "value")
    )
    def update_messages_table(selected_messages_date):
        messages = cache.load_raw_messages(selected_messages_date)
        if not messages.empty:
            return dbc.Table.from_dataframe(
                messages, striped=True, bordered=True, hover=True
            )
        return html.P("No messages to show")
