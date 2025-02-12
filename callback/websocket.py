# Callback del lado del cliente para actualizar el contenido en tiempo real
from dash import clientside_callback

from reactivity import in_websocket
from reactivity.storage.global_state import out_storage_global_state

clientside_callback(
  """
  (data) => {
    let [storage_global_state] = data;
    let btn = document.querySelector('#sync-trigger').click();
    return storage_global_state;
  }
  """,
  out_storage_global_state,
  in_websocket,
  prevent_initial_call=True
)
