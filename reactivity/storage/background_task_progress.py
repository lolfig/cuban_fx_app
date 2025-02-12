from dash import Input, Output
from dash.dcc import Store

storage_background_task_progress = Store(
  id='storage_background_task_progress',
  data=0
)
in_storage_background_task_progress = Input(
  storage_background_task_progress,
  "data"
)
out_storage_background_task_progress = Output(
  storage_background_task_progress,
  "data",
  allow_duplicate=True
)
