from dash import callback, dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_storage import data_store
from layouts.page_dashboard.outputs import out_slot_empirical_mode_decomposition
from reactivity import in_sync_trigger


@callback(out_slot_empirical_mode_decomposition, in_sync_trigger)
def update_slot_empirical_mode_decomposition(n_clicks):
    if data_store.imfs is None:
        return None

    imfs = data_store.imfs
    series = data_store.price_series
    series.index = pd.to_datetime(series.index)

    fig = make_subplots(
        rows=len(imfs) + 1,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,  # Espacio vertical entre plots
        subplot_titles=["USD/CUP - Serie Original"]
        + [f"IMF {i+1}" for i in range(len(imfs) - 1)]
        + ["Residuo"],
    )

    fig.add_trace(
        go.Scatter(
            x=series.index,
            y=series["USDCUP_Marginal"],
            line=dict(color="red"),
            name="Serie Original",
        ),
        row=1,
        col=1,
    )

    for n, imf_n in enumerate(imfs):
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=imf_n,
                line=dict(color="blue"),
                name=f"IMF {n+1}" if n < len(imfs) - 1 else "Residuo",
            ),
            row=n + 2,
            col=1,
        )

    fig.update_layout(
        height=2000,
        width=1220,
        title_text="Descomposición de Modos Empíricos",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")

    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))

    return dcc.Graph(figure=fig)
