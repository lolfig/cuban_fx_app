from dash import Output

from . import slot_messages_table, graph_histogram_vol_price, graph_supply_demand, slot_data_description, \
  slot_temporal_series, slot_info_cards, dropdown_messages_date, number_messages, main_dashboard_container

out_slot_messages_table = Output(slot_messages_table, "children")
out_pack_figure_graphs = [
  Output(graph_histogram_vol_price, "figure"),
  Output(graph_supply_demand, "figure")
]

out_slot_data_description = Output(
  slot_data_description,
  'children'
)

out_slot_temporal_series = Output(
  slot_temporal_series,
  'children'
)

out_slot_info_cards = Output(
  slot_info_cards,
  'children'
)

out_options_dropdown_messages_date = Output(
  dropdown_messages_date,
  "options"
)

out_value_dropdown_messages_date = Output(
  dropdown_messages_date,
  "value"
)
out_pack_options_value_dropdown_messages_date = [
  out_options_dropdown_messages_date,
  out_value_dropdown_messages_date
]

out_number_messages = Output(
  number_messages,
  "children"
)
out_main_dashboard_container = Output(
  main_dashboard_container,
  "children"
)
