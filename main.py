import uvicorn

from store import data_store  # noqa

if __name__ == '__main__':
  print("Iniciando dashboard...")
  uvicorn.run(
    "app:app",
    host='localhost',
    port=8000
  )
