import io
import zipfile
from os import path

from dash import callback, no_update, dcc

from config.const import DIR_DATA_MESSAGES
from layouts.layout_data_status.control_panel import in_dbc_save_btn
from reactivity import out_file_download
from services.framework_scraping.tools.missing_dates import get_existing_dates


def generate_buffer_zipfile():
  buffer = io.BytesIO()
  with zipfile.ZipFile(buffer, "w") as zip_file:
    # Agregar archivos al ZIP
    for file in get_existing_dates(DIR_DATA_MESSAGES):
      file_name = f"{file}.parquet"
      with open(path.join(DIR_DATA_MESSAGES, file_name), "rb") as f:
        zip_file.writestr(file_name, f.read())
        print(f"Added {file_name} to ZIP file")
  
  # Preparar el archivo ZIP para la descarga
  buffer.seek(0)
  return buffer


@callback(
  out_file_download,
  in_dbc_save_btn,
  prevent_initial_call=True
)
def download_file(n_clicks):
  if n_clicks == 0:
    print("n_clicks", n_clicks)
    return no_update
  print("download_file ....")
  buffer = generate_buffer_zipfile()
  return dcc.send_bytes(buffer.getvalue(), "save_data.zip")
