import dash_bootstrap_components as dbc
from dash import callback, html

from layouts.layout_dashboard import out_slot_messages_table, in_value_dropdown_messages_date
from services import cache as tools_cache


@callback(
  out_slot_messages_table,
  in_value_dropdown_messages_date
)
def update_messages_table(selected_messages_date):
  messages = tools_cache.load_raw_messages(selected_messages_date)
  if not messages.empty:
    return dbc.Table.from_dataframe(
      messages, striped=True, bordered=True, hover=True
    )
  return html.P("No messages to show")
