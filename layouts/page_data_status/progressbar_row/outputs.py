from dash import Output

from . import progressbar_sync_running, slot_fetch

out_value_progressbar__sync_running = Output(
  progressbar_sync_running,
  "value"
)
out_label_progressbar__sync_running = Output(
  progressbar_sync_running,
  "label"
)
out_animated_progressbar__sync_running = Output(
  progressbar_sync_running,
  "animated"
)
out_color_progressbar__sync_running = Output(
  progressbar_sync_running,
  "color"
)

out_pack_progressbar__sync_running = [
  out_value_progressbar__sync_running,
  out_label_progressbar__sync_running,
  out_animated_progressbar__sync_running,
  out_color_progressbar__sync_running
]

out_slot_slot_fetch = Output(
  slot_fetch,
  "children"
)
