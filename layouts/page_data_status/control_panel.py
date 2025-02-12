import dash_bootstrap_components as dbc
from dash import Input, dcc, State
from dash_iconify import DashIconify

layout = dbc.Row([
  dbc.Col(
    width=6,
    className="d-flex flex-row fill_with",
    children=(
      upload_btn := dcc.Upload(
        className="flex-grow-1 d-flex flex-row",
        multiple=True,
        children=dbc.Button(
          className="flex-grow-1",
          children=[
            DashIconify(
              icon="mdi:upload",
              className="me-2",
              width=30,
            ),
            "Subir"
          ],
          title="Upload data files",
          n_clicks=0
        )
      )),
  ),
  dbc.Col(
    children=[
      dbc_save_bt := dbc.Button(
        [
          DashIconify(
            icon="mdi:content-save",
            className="me-2",
            width=30,
          ),
          "Guardar"],
        title="Guardar",
        className="flex-grow-1",
        n_clicks=0
      ),
    ],
    className="d-flex flex-column",
    width=6
  )
])

in_pack_upload_btn = [
  Input(upload_btn, 'contents'),
  State(upload_btn, 'filename'),
  State(upload_btn, 'last_modified')
]
in_dbc_save_btn = Input(dbc_save_bt, "n_clicks")
