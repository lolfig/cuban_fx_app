from dash import Output

from . import progressbar_sync_running, slot_fetch

out_value_progressbar__sync_running = Output(
  progressbar_sync_running,
  "value"
)

out_slot_slot_fetch = Output(
  slot_fetch,
  "children"
)
