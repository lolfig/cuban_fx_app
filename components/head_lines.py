import dash_bootstrap_components as dbc
from dash import html


def row_h1(text):
  return dbc.Row(
    [
      dbc.Col(
        h1(text),
        className="mb-4 mt-2",
      )
    ]
  )


def h1(text):
  return html.H1(
    text,
    className="text-center",
  )


def row_h3(text):
  return dbc.Row(
    [
      dbc.Col(
        h3(text),
        className="mb-4 mt-2",
      )
    ]
  )


def h3(text):
  return html.H3(
    text,
    className="text-center",
  )
