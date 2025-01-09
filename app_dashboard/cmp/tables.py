from pandas import DataFrame
import dash_bootstrap_components as dbc
from dash import html


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
