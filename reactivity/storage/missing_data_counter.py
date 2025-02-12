from dash import Output, Input
from dash.dcc import Store

from app import data_store

storage_missing_data_counter = Store(
  id='missing_data_counter_storage',
  data=len(data_store.missing_dates)
)

in_storage_missing_data_counter = Input(
  storage_missing_data_counter,
  "data"
)

out_storage_missing_data_counter = Output(
  storage_missing_data_counter,
  "data",
  allow_duplicate=True
)
