import asyncio
import threading

from app import data_store


class SyncManager:
  
  @property
  def is_sync_running(self):
    if self.loop is None:
      return False
    elif not self.loop.is_running():
      return False
    return self.sync_data_task is not None and not self.sync_data_task.done()
  
  def run_forever_loop(self):
    # como esto está dentro de un thread, puedo poner mi loop nuevo,
    # este no es el hilo principal
    
    asyncio.set_event_loop(self.loop)
    self.loop.run_forever()
  
  def start_event_loop(self):
    # Crear un nuevo event loop y un hilo secundario
    self.loop = asyncio.new_event_loop()
    self.thread = threading.Thread(target=self.run_forever_loop, daemon=True)
    self.thread.start()
  
  def __init__(self):
    # Inicializar variables sin crear el hilo ni el event loop
    self.loop = None
    self.thread = None
    self.sync_data_task = None
    self.lock = threading.Lock()
  
  def run_sync_data(self):
    with self.lock:
      if self.loop is None or not self.loop.is_running():
        # Iniciar el event loop y el hilo si no están activos
        self.start_event_loop()
      
      if self.sync_data_task is None or self.sync_data_task.done():
        self.sync_data_task = asyncio.run_coroutine_threadsafe(
          data_store.sync_data(),
          self.loop
        )
        print("sync data task started")
      else:
        raise RuntimeError("sync data task is already running")
  
  def stop_sync_data(self):
    with self.lock:
      if self.sync_data_task is not None and not self.sync_data_task.done():
        # Paso 1: Cancelar la tarea
        self.sync_data_task.cancel()
        print("Cancelling sync data task ...")
        
        # Paso 2: Esperar a que la tarea termine
        try:
          # Forzar la finalización de la tarea
          self.loop.call_soon_threadsafe(self.sync_data_task.result)
        except asyncio.CancelledError:
          print("sync data task cancelled")
        except Exception as e:
          print(f"Error durante la cancelación: {e}")
      
      # Paso 3: Detener el event loop
      if self.loop is None:
        print("Event loop no iniciado.")
      
      elif self.loop.is_running():
        self.loop.call_soon_threadsafe(self.loop.stop)
        print("Event loop detenido.")
      
      if self.thread is None:
        print("Hilo secundario no iniciado.")
      # Paso 4: Esperar a que el hilo termine
      elif self.thread.is_alive():
        self.thread.join()
        print("Hilo secundario terminado.")
      
      # Limpiar referencias
      self.loop = None
      self.thread = None
      self.sync_data_task = None
      
      self.start_event_loop()
      if self.sync_data_task is None or self.sync_data_task.done():
        # aquí notifico el background task
        data_store.reload_from_file(True)
        self.sync_data_task = asyncio.run_coroutine_threadsafe(
          data_store.update_background_task_status(False),
          self.loop
        )


sync_manager = SyncManager()
