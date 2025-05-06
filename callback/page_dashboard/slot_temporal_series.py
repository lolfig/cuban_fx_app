import dash_bootstrap_components as dbc
from dash import callback, dcc, html, Input, Output
import pandas as pd
from plotly import express as px
import io

from data_storage import data_store
from layouts.page_dashboard.outputs import out_slot_temporal_series
from reactivity import in_sync_trigger


@callback(out_slot_temporal_series, in_sync_trigger)
def update_slot_temporal_series(n_clicks):
    if data_store.price_series is None or data_store.volumes_series is None:
        return []
    else:
        return [
            dbc.Col(
                dcc.Graph(
                    figure=px.line(
                        data_store.price_series.round(2), title="Serie de Precios"
                    )
                ),
                width=12,
            ),
            dbc.Col(
                dcc.Graph(
                    figure=px.line(
                        data_store.volumes_series.round(2),
                        title="Serie de Volúmenes",
                    )
                ),
                width=12,
            ),
            dbc.Col(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Descargar Serie de Precios",
                                id="download-price-button",
                                color="primary",
                                className="mt-3",
                                style={"fontSize": "16px", "padding": "10px 20px"},
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Descargar Serie de Volúmenes",
                                id="download-volumes-button",
                                color="primary",
                                className="mt-3",
                                style={"fontSize": "16px", "padding": "10px 20px"},
                            ),
                            width="auto",
                        ),
                    ],
                    justify="center",  # Centers the buttons horizontally
                ),
                width=12,
            ),
            dcc.Download(id="download-price-dataframe-xlsx"),
            dcc.Download(id="download-volumes-dataframe-xlsx"),
        ]


@callback(
    Output("download-price-dataframe-xlsx", "data"),
    Input("download-price-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_price_series(n_clicks):
    if data_store.price_series is not None:
        # Convert the DataFrame to an Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            data_store.price_series.to_excel(
                writer, index=False, sheet_name="PriceSeries"
            )
        output.seek(0)
        return dcc.send_bytes(output.read(), "price_series.xlsx")


@callback(
    Output("download-volumes-dataframe-xlsx", "data"),
    Input("download-volumes-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_volumes_series(n_clicks):
    if data_store.volumes_series is not None:
        # Convert the DataFrame to an Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            data_store.volumes_series.to_excel(
                writer, index=False, sheet_name="VolumesSeries"
            )
        output.seek(0)
        return dcc.send_bytes(output.read(), "volumes_series.xlsx")
