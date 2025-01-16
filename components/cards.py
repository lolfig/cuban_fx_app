from dash import html

# custom_components
from dash_bootstrap_components import (
  Card,
  CardHeader,
  CardBody
)


def basic_card(title, body):
  return Card(
    [
      CardHeader(title),
      CardBody(
        [
          html.P(body, className="card-text"),
        ]
      ),
    ],
    style={"height": "100px"},
  )
