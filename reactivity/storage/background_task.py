from dash import Input, Output, State
from dash.dcc import Store

from app import data_store

storage_background_task = Store(
  id='storage_background_task',
  data=data_store.background_task
)
in_storage_background_task = Input(
  storage_background_task,
  "data"
)
out_storage_background_task = Output(
  storage_background_task,
  'data',
  allow_duplicate=True
)
state_storage_background_task = State(storage_background_task, "data")
