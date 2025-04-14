import uvicorn

from data_storage import data_store  # noqa

if __name__ == '__main__':
  print("Iniciando dashboard...")
  uvicorn.run(
    "app:app",
    host='0.0.0.0',
    port=8000
  )
