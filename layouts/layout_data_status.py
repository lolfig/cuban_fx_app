import calendar
from itertools import chain

import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, Output, Input, dcc, State
from dash_iconify import DashIconify

from app import data_store
from components import head_lines as custom_head_lines


def generate_git_hub_days_counter_content():
  df = pd.DataFrame(
    data_store.dates,
    columns=['date', 'value']
  )
  
  date_range = pd.to_datetime(df['date']).dt
  week = date_range.isocalendar().week
  
  df['date'] = date_range
  df['month'] = date_range.month.map(lambda x: calendar.month_abbr[x])
  df['year'] = date_range.year
  df["weekday"] = date_range.weekday.map(lambda x: calendar.day_abbr[x])
  df["week"] = week.where(~((week > 5) & (date_range.month == 1)), 0)
  
  df_pivot = df.pivot_table(
    index=['year', 'weekday'],
    columns=['week'],
    values=['value'],
    aggfunc='first'
  )
  
  df_pivot.columns = pd.MultiIndex.from_frame(
    df[['month', 'week']].groupby('week').agg('first').reset_index()[['month', 'week']])
  content = [
    [
      dbc.Col(
        custom_head_lines.h3(year_selected),
        width=12,
      ),
      dbc.Col(
        create_table(df_pivot, year_selected),
        class_name="overflow-auto",
        width=12,
      ),
    ]
    for year_selected in df['year'].drop_duplicates().sort_values()
  ]
  
  return dbc.Container(
    dbc.Row(
      children=[*chain(*content)]
    )
  )


def create_table(df_pivot, year_selected):
  box_size = '17px'
  
  resume = df_pivot.loc[
    [(year_selected, calendar.day_abbr[i])
     for i in range(7)]
  ]
  header = html.Thead(
    children=html.Tr(
      style={
        "height": "13px"
      },
      children=[
        html.Td(
          style={
            "min-width": "35px",
          },
        ), *[
          html.Td(
            children=calendar.month_abbr[month + 1],
            colSpan=4
          )
          for month in range(12)
        ]]
    )
  )
  rows = html.Tbody([
    html.Tr(
      style={
        "height": box_size,
        "position": "relative"
      },
      children=[
        html.Td(
          html.Span(
            "" if ix % 2 else week_day,
            style={
              "clip-path": None,
              "position": "absolute",
              "bottom": "-3px"
            }
          )
        ),
        *[
          html.Td(
            style={
              "min-width": box_size,
              "border-radius": "2px",
              "outline-offset": "-1px",
              "shape-rendering": "geometricPrecision",
              "background-color": color_by_value(value),
            },
            children=None,
          )
          for value in resume.loc[(year, week_day)]
        ]
      ]) for ix, (year, week_day) in enumerate(resume.index)
  ])
  # Generar los elementos
  elements = html.Table([
    header,
    rows
  ],
    style={
      "border-spacing": "3px",
      "overflow": "hidden",
      "position": "relative",
      "width": "max-content",
      "border-collapse": "separate"
    }
  )
  return elements


def color_by_value(value):
  if value != value:
    return "transparent"
  return "green" if value else "red"


slot_git_hub_days_counter = html.Div()
out_slot_git_hub_days_counter = Output(
  slot_git_hub_days_counter,
  'children'
)

fetch_btn = dbc.Button(
  [
    DashIconify(
      icon="mdi:sync",
      className="me-2",
      width=30,
    ),
    "Sincronizar"],
  className="flex-grow-1",
  n_clicks=0
)

in_click_fetch_btn = Input(
  fetch_btn,
  "n_clicks"
)

fetching_btn = dbc.Button(
  children=[
    DashIconify(
      icon="mdi:sync",
      className="me-2",
      width=30,
    ),
    "Sincronizando"],
  disabled=True,
  className="flex-grow-1",
  n_clicks=0
)

slot_fetch = dbc.Col(
  className="d-flex flex-column",
  width=4
)

out_slot_slot_fetch = Output(
  slot_fetch,
  "children"
)

upload_btn = dcc.Upload(
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
    n_clicks=0
  )
)
in_pack_upload_btn = [
  Input(upload_btn, 'contents'),
  State(upload_btn, 'filename'),
  State(upload_btn, 'last_modified')
]

actions_btns = dbc.Row([
  dbc.Col(
    width=4,
    className="d-flex flex-row fill_with",
    children=upload_btn,
  ),
  slot_fetch,
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
        className="flex-grow-1",
        n_clicks=0
      ),
    ],
    className="d-flex flex-column",
    width=4
  )
]
)

in_dbc_save_btn = Input(dbc_save_bt, "n_clicks")

layout = dbc.Container([
  custom_head_lines.row_h1("Cargador de datos"),
  actions_btns,
  slot_git_hub_days_counter
])
