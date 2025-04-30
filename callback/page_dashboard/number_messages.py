from dash import callback, dcc
from plotly import express as px

from data_storage import data_store
from layouts.page_dashboard.outputs import out_number_messages
from reactivity import in_sync_trigger


@callback(out_number_messages, in_sync_trigger)
def update_number_messages(n_clicks):
    if data_store.number_messages is None:
        return None
    return dcc.Graph(
        figure=px.line(
            data_store.number_messages.round(2),
        )
    )
