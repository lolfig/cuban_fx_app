from typing import List
import pickle

import pandas as pd

from tools.const import CURRENCIES
from framework_scraping.tools.fetcher import fetch_exchange_rate_data


class PriceTimeSeries:
    def __init__(self, start_date: str, end_date: str, path: str, offers: List[str], currency: CURRENCIES):
        self.start_date = start_date
        self.end_date = end_date
        self.path = path
        self.offers = offers
        self.currency = currency
        self.toque_serie = pd.DataFrame()
        self.toque_all_info = {}

    def get_time_series(self):
        """
        Fetches and processes exchange rate data to create a time series DataFrame.
        
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

    def _construct_api_url(self, offer: str) -> str:
        """
        Constructs the API URL for fetching exchange rate data.

        Args:
            offer (str): Indicates the type of exchange rate ("Compra" or "Venta").

        Returns:
            str: The constructed API URL.
        """
        return (
            f"https://api.cambiocuba.money/api/v1/x-rates-by-date-range-history?"
            f"trmi=true&cur={self.currency}&offer={offer}&"
            f"date_from={self.start_date} 00:00:00&date_to={self.end_date} 00:00:00"
        )

    def _process_offer_data(self, data_toque: List[dict], offer: str) -> pd.DataFrame:
        """
        Processes raw exchange rate data to create a time series DataFrame without missing dates.

        Args:
            data_toque (List[Dict[str, Any]]): Raw data fetched from the API.
            offer (str): Indicates whether the data is for "Compra" or "Venta".

        Returns:
            pd.DataFrame: A cleaned DataFrame containing the time series with interpolated values.
        """
        serie = pd.DataFrame(
            {
                'date': [pd.to_datetime(d['_id']) for d in data_toque],
                f'{self.currency}CUP{offer}': [d['median'] for d in data_toque]
            }
        )

        date_range_df = pd.DataFrame(
            {
                'date': pd.date_range(start=serie['date'].min(), end=serie['date'].max(), freq='D')
            }
        )

        merged_df = date_range_df.merge(
            serie, on='date', how='left'
        ).interpolate(method='linear').drop_duplicates('date').reset_index(drop=True)

        return merged_df

    def save_data_info(self):
        """
        Saves the time series DataFrame and additional information to pickle files.
        
        The main DataFrame is saved with its index set to 'date', and all additional 
        information is stored in a separate pickle file.
        """
        data = self.toque_serie.copy()

        data.set_index('date', inplace=True)

        # saving toque_serie
        data.to_pickle(f"{self.path}/{self.currency}CUP.pickle")

        # save toque_all_info
        with open(f'{self.path}/all_info_{self.currency}CUP.pickle', 'wb') as file:
            pickle.dump(self.toque_all_info, file)
