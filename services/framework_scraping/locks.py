import os
import asyncio
import time

DEFAULT_LOCK_PATH = os.path.join(os.getcwd(), "data", ".scraper.lock")


class AsyncFileLock:
    """
    Lock de archivo asincrónico por sondeo (polling) con creación atómica del archivo.
    - Si el lock existe, espera hasta que quede libre (timeout=None => espera indefinida).
    - Uso:
        async with AsyncFileLock(DEFAULT_LOCK_PATH):
            # sección crítica
    """
    def __init__(self, path: str, poll_interval: float = 0.5, timeout: float | None = None):
        self.path = path
        self.poll_interval = poll_interval
        self.timeout = timeout
        self._fd = None

        # Asegura que el directorio destino exista
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    async def acquire(self):
        start = time.time()
        while True:
            try:
                # O_CREAT | O_EXCL -> crea el archivo de forma atómica, falla si ya existe
                self._fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                # Escribimos el PID para depuración
                os.write(self._fd, str(os.getpid()).encode())
                return
            except FileExistsError:
                if self.timeout is not None and (time.time() - start) > self.timeout:
                    raise TimeoutError(f"No se pudo adquirir el lock en {self.path} dentro del tiempo de espera")
                await asyncio.sleep(self.poll_interval)

    async def release(self):
        try:
            if self._fd is not None:
                os.close(self._fd)
                self._fd = None
            if os.path.exists(self.path):
                os.unlink(self.path)
        except FileNotFoundError:
            # ya se liberó
            pass

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.release()