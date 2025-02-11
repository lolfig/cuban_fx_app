from dash import clientside_callback

from reactivity import (
  in_websocket
)
from reactivity.storage.background_task import out_storage_background_task
from reactivity.storage.global_state import out_storage_global_state
from reactivity.storage.missing_data_counter import out_storage_missing_data_counter

# Callback del lado del cliente para actualizar el contenido en tiempo real
clientside_callback(
  """
  ([
    background_task_status,
    missing_data_counter,
    storage_global_state
  ]) => {
    return [
      background_task_status,
      missing_data_counter,
      storage_global_state
    ];
  }
  """,
  [
    out_storage_background_task,
    out_storage_missing_data_counter,
    out_storage_global_state,
  ],
  in_websocket,
  prevent_initial_call=True
)
