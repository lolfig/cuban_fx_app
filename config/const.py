import datetime
import os
from typing import Literal

today = datetime.datetime.now().date()
yesterday = today - datetime.timedelta(days=1)

# CONST
CURRENCIES = Literal['USD', 'EUR']

DIR_DATA_ANALYTICS = os.path.join(os.getcwd(), "data", "analytics")
DIR_DATA_MESSAGES = os.path.join(os.getcwd(), "data", "messages")

for directory in [
  DIR_DATA_ANALYTICS,
  DIR_DATA_MESSAGES
]:
  os.makedirs(directory, exist_ok=True)
ACTIVATE_INTERVAL = False
DEACTIVATE_INTERVAL = True
MISSING_DATE_BADGE_COLOR = "danger"
SHOW_INLINE_BLOCK = {"display": "inline-block"}
HIDDE = {"display": "none"}

# Timeout por defecto para el lock de scrapers (None => espera indefinida)
SCRAPER_LOCK_TIMEOUT_SEC = None
