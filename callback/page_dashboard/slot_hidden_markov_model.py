from dash import callback, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_storage import data_store
from layouts.page_dashboard.outputs import out_slot_hidden_markov_model
from reactivity import in_sync_trigger


@callback(out_slot_hidden_markov_model, in_sync_trigger)
def update_slot_hidden_markov_model(n_clicks):
    if data_store.hmm is None:
        return None

    data_frame = data_store.hmm

    # Obtener los estados únicos
    states = data_frame["States"].unique()

    # Definir una paleta de colores consistente para los estados
    color_palette = [
        "blue",
        "red",
    ]  # Puedes personalizar esta lista según tus preferencias
    state_colors = {state: color_palette[i] for i, state in enumerate(states)}

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Precios por Estado", "Retornos por Estado"),
        shared_xaxes=True,
        vertical_spacing=0.1,
    )

    # Gráfico 1: Precios de la moneda por estado
    for state in states:
        state_data = data_frame[data_frame["States"] == state]
        fig.add_trace(
            go.Scatter(
                x=state_data["Time"],
                y=state_data["Currency"],
                mode="markers",
                name=f"Estado {state}",
                marker=dict(
                    size=6, color=state_colors[state]
                ),  # Asignar color por estado
            ),
            row=1,
            col=1,
        )

    # Gráfico 2: Retornos de la moneda por estado
    for state in states:
        state_data = data_frame[data_frame["States"] == state]
        fig.add_trace(
            go.Scatter(
                x=state_data["Time"],
                y=state_data["Returns"],
                mode="markers",
                name=f"Estado {state}",
                marker=dict(
                    size=6, color=state_colors[state]
                ),  # Asignar color por estado
                showlegend=False,  # Evitar duplicar leyendas
            ),
            row=2,
            col=1,
        )

    # Configurar diseño de los gráficos
    fig.update_xaxes(title_text="Tiempo", row=1, col=1)
    fig.update_yaxes(title_text="Precio", row=1, col=1)
    fig.update_xaxes(title_text="Tiempo", row=2, col=1)
    fig.update_yaxes(title_text="Retornos", row=2, col=1)

    fig.update_layout(
        height=800,
        width=1220,
        title_text="Análisis del Modelo Oculto de Markov",
        showlegend=True,
    )
    return dcc.Graph(figure=fig)
