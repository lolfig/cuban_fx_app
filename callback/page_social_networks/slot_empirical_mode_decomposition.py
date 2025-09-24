from dash import callback, dcc, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_storage import data_store
from reactivity import in_sync_trigger

@callback(Output("tg-slot-empirical-mode-decomposition", "children"), in_sync_trigger)
def update_tg_slot_empirical_mode_decomposition(n_clicks):
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

    # Añadir cada IMF como un subplot
    for i, imf in enumerate(imfs):
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=imf,
                line=dict(color="blue"),
                name=f"IMF {i+1}" if i < len(imfs) - 1 else "Residuo",
            ),
            row=i + 2,
            col=1,
        )

    # Configurar diseño
    fig.update_layout(
        height=1200,  # Altura total del gráfico
        width=1220,  # Ancho del gráfico
        title_text="Descomposición de Modos Empíricos (EMD)",
        showlegend=False,
    )

    return dcc.Graph(figure=fig)