import asyncio
import threading
from functools import wraps
from typing import Callable, Coroutine

from dash import callback, no_update

from app import data_store
from layouts.layout_data_status import in_click_fetch_btn
from reactivity import out_storage_background_task


# Función que ejecuta la Coroutine en un nuevo loop
def await_function(fun: Callable[[Exception], Coroutine[None, None, None]]):
  @wraps(fun)
  def decorator(*args, **kwargs) -> None:
    loop = asyncio.new_event_loop()  # Creamos un nuevo loop
    asyncio.set_event_loop(loop)  # Asociamos el loop al hilo
    loop.run_until_complete(fun(*args, **kwargs))  # Ejecutamos la tarea
  
  return decorator


@await_function
async def notify_fail(e: Exception):
  print(e)
  print("La actualización falló!!")
  await data_store.update_background_task_status(False)


class ThreadWithFallBack(threading.Thread):
  def __init__(
    self,
    fallback: Callable[[Exception], None],
    **kwargs: object
  ):
    super().__init__(**kwargs)
    self.fallback = fallback
  
  def run(self):
    try:
      super().run()
    except Exception as e:
      print(e)
      self.fallback(e)


@callback(
  out_storage_background_task,
  in_click_fetch_btn,
  prevent_initial_call=True
)
def run_fetch(n_clicks):
  if n_clicks == 0:
    return no_update
  hilo = ThreadWithFallBack(
    fallback=notify_fail,  # noqa
    target=await_function(data_store.sync_data),
    daemon=True
  )
  hilo.start()
  return True
