
from functools import partial
from dash import html

LOGO_IMG_STYLE = {
    "display": "block",
    "margin": "0 auto",
    "width": "150px",
}

logo_image = partial(
    html.Img,
    style=LOGO_IMG_STYLE,
)