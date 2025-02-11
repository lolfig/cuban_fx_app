import calendar

from pandas import DataFrame
import dash_bootstrap_components as dbc
from dash import html

from components.tools import color_by_value


def table_head(title: str, data: DataFrame, col_with=4) -> dbc.Col:
    return dbc.Col(
        [
            html.H4(title),
            dbc.Table.from_dataframe(
                data.round(2),
                striped=True,
                bordered=True,
                hover=True,
            ),
        ],
        width=col_with,
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
