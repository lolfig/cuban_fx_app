from . import (
  storages,
  websocket,
  router_view,
  navigation_drawer,
  badge_missing_days,
  badge_indicator_missing_days,
  page_data_status,
  page_dashboard,
  page_settings
)
from .page_data_status_telegram import __init__ as _page_data_status_telegram  # registra callbacks de la página de Telegram
from .page_social_networks import __init__ as _page_social_networks  # NUEVO: registra callbacks de Redes Sociales
