from dash import callback
from plotly import graph_objects as go

from app import data_store
from layouts.page_dashboard.outputs import out_pack_figure_graphs
from layouts.page_dashboard.inputs import in_value_dropdown_date
from services import formaters


@callback(
  out_pack_figure_graphs,
  in_value_dropdown_date,
)
def update_daily_histograms(selected_date):
  if selected_date is None:
    return {}, {}
  
  if selected_date and (selected_date in data_store.daily_data):
    fig1 = go.Figure()
    fig1.add_trace(
      go.Scatter(
        x=data_store.daily_data[selected_date]["Compras_ordenadas"].index,
        y=data_store.daily_data[selected_date]["Compras_ordenadas"].values,
        mode="lines+markers",
        name="Demanda (Compra)",
        line=dict(color="blue"),
      )
    )
    fig1.add_trace(
      go.Scatter(
        x=data_store.daily_data[selected_date]["Ventas_ordenadas"].index,
        y=data_store.daily_data[selected_date]["Ventas_ordenadas"].values,
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
        x=data_store.daily_data[selected_date]["Nivel_volumen_compra"],
        y=data_store.daily_data[selected_date]["Nivel_precio_compra"],
        mode="lines",
        name="Demanda (Compras)",
        line=dict(color="blue"),
      )
    )
    fig2.add_trace(
      go.Scatter(
        x=data_store.daily_data[selected_date]["Nivel_volumen_venta"],
        y=data_store.daily_data[selected_date]["Nivel_precio_venta"],
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
