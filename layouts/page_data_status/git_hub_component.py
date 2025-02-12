from dash import html, Output

slot_git_hub_days_counter = html.Div()

out_slot_git_hub_days_counter = Output(
  slot_git_hub_days_counter,
  'children'
)
