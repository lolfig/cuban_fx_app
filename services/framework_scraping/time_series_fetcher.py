import os.path
import pickle
from typing import List

import pandas as pd

from config.const import CURRENCIES
from services.framework_scraping.tools.fetcher import fetch_exchange_rate_data


class PriceTimeSeries:
  def __init__(
    self,
    start_date: str,
    end_date: str,
    path: str,
    offers: List[str],
    currency: CURRENCIES
  ):
    self.start_date = start_date
    self.end_date = end_date
    self.path = path
    self.offers = offers
    self.currency = currency
    self.toque_serie = pd.DataFrame()
    self.toque_all_info = {}
  
  def sync_time_series(self):
    """
    Fetches, processes and Save!!! exchange rate data to create a time series DataFrame.
    
    This method iterates through the specified offers, constructs the API URLs,
    fetches the corresponding exchange rate data, processes it into a time series,
    and merges all results into a single DataFrame.
    """
    for offer in self.offers:
      api_url = self._construct_api_url(offer)
      data_toque = fetch_exchange_rate_data(api_url)
      if data_toque is not None:
        self.toque_all_info[offer] = pd.DataFrame(data_toque)
        merged_df = self._process_offer_data(data_toque, offer)
        self.toque_serie = pd.merge(
          self.toque_serie,
          merged_df,
          on='date',
          how='outer'
        ) if not self.toque_serie.empty else merged_df
    self.save_data_info()
    return self
  
  def _construct_api_url(self, offer: str) -> str:
    return (
      f"https://api.cambiocuba.money/api/v1/x-rates-by-date-range-history?"
      f"trmi=true&cur={self.currency}&offer={offer}&"
      f"date_from={self.start_date} 00:00:00&date_to={self.end_date} 00:00:00"
    )
  
  def _process_offer_data(self, data_toque: List[dict], offer: str) -> pd.DataFrame:
    serie = pd.DataFrame({
      'date': [
        pd.to_datetime(d['_id']) for d in data_toque
      ],
      f'{self.currency}CUP{offer}': [
        d['median'] for d in data_toque
      ]
    }
    )
    
    date_range_df = pd.DataFrame({
      'date': pd.date_range(
        start=serie['date'].min(),
        end=serie['date'].max(),
        freq='D'
      )
    })
    
    merged_df = date_range_df.merge(
      serie, on='date', how='left'
    ).interpolate(method='linear').drop_duplicates('date').reset_index(drop=True)
    
    return merged_df
  
  def save_data_info(self):
    with open(
      os.path.join(
        self.path,
        f'{self.currency}CUP.pickle'
      ),
      'wb'
    ) as file:
      pickle.dump(self, file)  # noqa este file es writeable
  
  @staticmethod
  def load_from_file(path, currency) -> "PriceTimeSeries":
    with open(
      os.path.join(
        path,
        f'{currency}CUP.pickle'
      ),
      'rb'
    ) as file:
      return pickle.load(file)  # noqa este file es readable
