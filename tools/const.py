import datetime
import os
from typing import Literal

today = datetime.datetime.now().date()
yesterday = today - datetime.timedelta(days=1)

# CONST
CURRENCIES = Literal['USD', 'EUR']

DIR_DATA_ANALYTICS = os.path.join(os.getcwd(), "data/analytics")

DIR_DATA_MESSAGES = os.path.join(os.getcwd(), "data/messages")

for directory in [
    DIR_DATA_ANALYTICS,
    DIR_DATA_MESSAGES
]:
    os.makedirs(directory, exist_ok=True)

LOGO = os.path.join(os.getcwd(), "assets/logo.png")
