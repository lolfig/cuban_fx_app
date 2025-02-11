import dash
from dash import callback, dcc
from plotly import express as px

from layouts.layout_dashboard.outputs import out_number_messages
from reactivity.storage.global_state import in_storage_global_state, state_storage_global_state
from store import data_store


@callback(
  out_number_messages,
  in_storage_global_state,
  state_storage_global_state
)
def update_number_messages(global_state, last_global_state):
  if global_state == last_global_state:
    return dash.no_update
  if data_store.number_messages is None:
    return None
  
  return dcc.Graph(
    figure=px.line(
      data_store.number_messages.round(2),
    )
  )
