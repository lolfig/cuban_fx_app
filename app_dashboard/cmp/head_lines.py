import dash_bootstrap_components as dbc
from dash import html


def h1(text):
    return dbc.Row(
        [
            dbc.Col(
                html.H1(
                    text,
                    className="text-center",
                ),
                className="mb-4 mt-2",
            )
        ]
    )


def h3(text):
    return dbc.Row(
        [
            dbc.Col(
                html.H3(
                    text,
                    className="text-center",
                ),
                className="mb-4 mt-2",
            )
        ]
    )
