import dash_bootstrap_components as dbc
from dash import html


def basic_card(title, body):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(
                [
                    html.P(body, className="card-text"),
                ]
            ),
        ],
        style={"height": "100px"},
    )
