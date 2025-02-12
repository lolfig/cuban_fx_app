from dash import Input, Output, State
from dash.dcc import Store

storage_global_state = Store(
  'global-state',
  data=None
)

in_storage_global_state = Input(
  storage_global_state,
  'data'
)

out_storage_global_state = Output(
  storage_global_state,
  'data',
  allow_duplicate=True
)
state_storage_global_state = State(
  storage_global_state,
  'data'
)
