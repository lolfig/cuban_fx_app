# Corutina asincrónica con generador
from collections.abc import Coroutine


async def f1(x) -> Coroutine[str, int, str]:
  while x > 0:
    print(f"Empezando ciclo con x = {x}")
    result = yield x - 1  # Generamos un valor y suspendemos
    print(f"Recibido en la corutina: {result}")
    x -= 1
  return 'Terminé'


async def main():
  coro = f1(5)
  
  # Llamamos a `__anext__` para avanzar la corutina hasta el primer `yield`
  print(await coro.__anext__())  # Ejecuta hasta el primer yield, devuelve 4
  
  # Ahora enviamos un valor de vuelta a la corutina con `asend`
  print(await coro.asend("Valor recibido"))  # Ejecuta hasta el siguiente yield y devuelve 3
  
  # Continuamos con la corutina
  print(await coro.asend("Otro valor"))  # Devuelve 2
  
  # Y así sucesivamente
  print(await coro.asend("Final"))
  
  try:
    # Terminamos la corutina
    print(await coro.asend("Chao"))  # La corutina termina, lanzando StopAsyncIteration
  except StopAsyncIteration as e:
    print(f"Corutina terminó con valor: {e.value}")


# Ejecutamos el código en un entorno asíncrono
await main()
