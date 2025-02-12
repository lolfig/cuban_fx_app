import dash_bootstrap_components as dbc

from components import head_lines as custom_head_lines
from . import control_panel
from . import git_hub_component
from . import progressbar_row



layout = dbc.Container([
  custom_head_lines.row_h1("Cargador de datos"),
  progressbar_row.layout,
  control_panel.layout,
  git_hub_component.slot_git_hub_days_counter
])
