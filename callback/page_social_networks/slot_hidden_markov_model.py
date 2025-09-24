from dash import callback, dcc, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from hmmlearn import hmm

from data_storage import data_store
from layouts.page_social_networks import tg_slot_hidden_markov_model
from reactivity import in_sync_trigger


@callback(
    Output(tg_slot_hidden_markov_model, "children"),
    in_sync_trigger
)
def update_tg_slot_hidden_markov_model(n_clicks):
    # Usar datos de Telegram en lugar de El Toque
    if data_store.telegram_analytics is None or data_store.telegram_analytics.empty:
        return None
    
    # Crear un dataframe con los precios de venta de Telegram
    analytics = data_store.telegram_analytics
    
    # Extraer fechas y precios de venta
    dates = []
    prices = []
    
    for date in analytics.index:
        if len(analytics.loc[date]["Precio_Venta"]) > 0:
            # Usar el promedio de precios de venta para cada día
            avg_price = np.mean(analytics.loc[date]["Precio_Venta"])
            dates.append(date)
            prices.append(avg_price)
    
    if len(dates) < 3:  # Necesitamos al menos algunos puntos para el HMM
        return None
    
    # Crear dataframe para HMM
    data_frame = pd.DataFrame({
        "Time": pd.to_datetime(dates),
        "Currency": prices,
        "Returns": pd.Series(prices).diff().values
    })
    data_frame.dropna(inplace=True)
    
    # Si no hay suficientes datos después de eliminar NaN, retornar None
    if len(data_frame) < 3:
        return None
    
    # Aplicar HMM
    returns = data_frame[["Returns"]].values
    model = hmm.GaussianHMM(
        n_components=2,  # 2 estados
        covariance_type="full",
        n_iter=50,
        random_state=42,
        algorithm="map",
    )
    
    try:
        model.fit(returns)
        Z = model.predict(returns)
        data_frame["States"] = Z
    except:
        # Si hay error en el HMM, mostrar mensaje
        return "No hay suficientes datos para el modelo HMM"
    
    # Obtener los estados únicos
    states = data_frame["States"].unique()

    # Definir una paleta de colores consistente para los estados
    color_palette = ["blue", "red"]  # Puedes personalizar esta lista según tus preferencias
    state_colors = {state: color_palette[i] for i, state in enumerate(states)}

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Precios por Estado (Telegram)", "Retornos por Estado (Telegram)"),
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
                marker=dict(size=6, color=state_colors[state]),  # Asignar color por estado
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
                marker=dict(size=6, color=state_colors[state]),  # Asignar color por estado
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
        title_text="Análisis del Modelo Oculto de Markov (Telegram)",
        showlegend=True,
    )
    return dcc.Graph(figure=fig)