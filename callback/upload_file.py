import base64
from os import path

from dash import callback

from config.const import DIR_DATA_MESSAGES
from layouts.layout_data_status import in_pack_upload_btn


def parse_contents(content, filename, date):
  data = content.encode("utf8").split(b";base64,")[1]
  
  try:
    if filename.endswith(".parquet"):
      # data = content.encode("utf8").split(b";base64,")[1]
      with open(path.join(DIR_DATA_MESSAGES, filename), "wb") as fp:
        fp.write(base64.decodebytes(data))
  except Exception as e:
    print(e)


@callback(
  in_pack_upload_btn
)
def update_output(list_of_contents, list_of_names, list_of_dates):
  if list_of_contents is not None:
    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
      parse_contents(c, n, d)
