import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from services.framework_analytics.analytics_utils import find_marginal_price


def _extract_orders(df):
  """
  Extracts buy and sell orders from the DataFrame.

  Args:
      df (pd.DataFrame): DataFrame containing formal orders.

  Returns:
      tuple: Two DataFrames containing buy and sell orders respectively.
  """
  
  buy_orders = [
    {"vol_compra": order["size"], "precio_compra": order["price"]}
    for order in df["orders"]
    if order and order["sign"] == "compro"
  ]
  sell_orders = [
    {"vol_venta": order["size"], "precio_venta": order["price"]}
    for order in df["orders"]
    if order and order["sign"] == "vendo"
  ]
  all_orders = [
    {"sign": order["sign"], "price": order["price"], "volume": order["size"]}
    for order in df["orders"]
    if order and 45 < order["price"] < 500 and 0 <= order["size"] < 50000
  ]
  
  return pd.DataFrame(buy_orders), pd.DataFrame(sell_orders), all_orders


def _calculate_levels(orders_df, is_sell=False):
  """
  Calculates cumulative volume and price levels from orders.

  Args:
      orders_df (pd.DataFrame): DataFrame containing formal orders.
      is_sell (bool): Indicates whether to process sell orders. Defaults to False.

  Returns:
      tuple: Two numpy arrays representing cumulative volume and price levels.
  """
  if is_sell:
    orders_df.sort_values(by="precio_venta", inplace=True)
  else:
    orders_df.sort_values(by="precio_compra", ascending=False, inplace=True)
  
  volumen_nivel = np.array(
    orders_df["vol_compra" if not is_sell else "vol_venta"].cumsum()
  )
  precio_nivel = np.array(orders_df[orders_df.columns[1]].tolist())
  
  return volumen_nivel, precio_nivel


def _group_orders(orders_df):
  """
  Groups orders by price levels.

  Args:
      orders_df (pd.DataFrame): DataFrame containing formal orders.

  Returns:
      pd.Series: Series with grouped order volumes by price.
  """
  return (
    orders_df.apply(lambda x: 5 * round(x / 5.0))
    .groupby(orders_df.columns[1])[  # Agrupar por precio
      "vol_compra" if "compra" in orders_df.columns[1] else "vol_venta"
    ]
    .sum()
    .replace(0, np.nan)
    .dropna()
  )


def _do_intra_day_analytics(date, compra_df, venta_df):
  """
  Analyzes intraday data to calculate stylized facts.

  Args:
      df (pd.DataFrame): DataFrame containing processed messages and orders.
      date (str): The date corresponding to the data being analyzed.

  Returns:
      pd.DataFrame: A DataFrame containing calculated stylized facts for the day.
  """
  
  # Calculate volume and price levels
  nivel_volumen_compra, nivel_precio_compra = _calculate_levels(compra_df)
  nivel_volumen_venta, nivel_precio_venta = _calculate_levels(
    venta_df, is_sell=True
  )
  
  price, vol = find_marginal_price(
    nivel_precio_compra,
    nivel_volumen_compra,
    nivel_precio_venta,
    nivel_volumen_venta,
  )
  marginal_data = [{"price_mar": price, "vol_mar": vol}]
  
  # Group orders for histogram plot
  grouped_buy = _group_orders(compra_df)
  grouped_sell = _group_orders(venta_df)
  
  analytics = {
    "Compras_ordenadas": grouped_buy[grouped_buy >= 500],
    "Ventas_ordenadas": grouped_sell[grouped_sell >= 500],
    "Nivel_volumen_compra": nivel_volumen_compra,
    "Nivel_precio_compra": nivel_precio_compra,
    "Nivel_volumen_venta": nivel_volumen_venta,
    "Nivel_precio_venta": nivel_precio_venta,
    "Marginal_Data": marginal_data,
    "Volumen_Compra": sum(compra_df["vol_compra"]),
    "Volumen_Venta": sum(venta_df["vol_venta"]),
    "Volumen_Total": sum(compra_df["vol_compra"]) + sum(venta_df["vol_venta"]),
    "Cantidad_Compra": compra_df["vol_compra"].tolist(),
    "Cantidad_Venta": venta_df["vol_venta"].tolist(),
    "Precio_Compra": compra_df["precio_compra"].tolist(),
    "Precio_Venta": venta_df["precio_venta"].tolist(),
  }
  
  return pd.DataFrame([analytics], index=[date])


@dataclass(frozen=True)
class DataAnalytics:
  dataframe: pd.DataFrame
  orders: dict
  
  @classmethod
  def do_analytics(cls, path)->"DataAnalytics":
    """
    Performs framework_analytics on processed messages and formal orders.

    This method reads all parquet files from the specified path,
    processes each file to extract relevant framework_analytics, and
    compiles the results into a single DataFrame.
    """
    data_frames = []
    orders = {}
    for file in os.listdir(path):
      if file.endswith(extension := ".parquet"):
        date = file[:-len(extension)]
        df = pd.read_parquet(
          os.path.join(
            path,
            file
          )
        )
        compra_df, venta_df, all_orders = _extract_orders(df)
        orders[date] = all_orders
        
        intraday_data = _do_intra_day_analytics(date, compra_df, venta_df)
        data_frames.append(intraday_data)
    dataframe = pd.concat(data_frames)
    dataframe.index = pd.to_datetime(dataframe.index)
    dataframe.sort_index(inplace=True)
    return cls(
      dataframe=pd.concat(data_frames),
      orders=orders
    )
