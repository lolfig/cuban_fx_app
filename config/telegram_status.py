import json
import os
from datetime import datetime, timezone

STATUS_FILE = 'data/telegram_channels_status.json'


def _ensure_dir():
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)


def load_status():
    _ensure_dir()
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
    # Si no existe o está corrupto, crear archivo vacío
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=2)
    return {}


def save_status(status: dict):
    _ensure_dir()
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def update_channel_status(channel_url: str, *, status: str, new_messages: int, total_messages: int, last_error: str = ""):
    """
    Actualiza el estado de un canal específico.
    status: "ok" | "error"
    """
    data = load_status()

    now = datetime.now(timezone.utc).isoformat()
    data[channel_url] = {
        "channel": channel_url,
        "status": status,
        "last_run": now,
        "new_messages": int(new_messages),
        "total_messages": int(total_messages),
        "last_error": last_error,
    }

    save_status(data)


def get_all_channels_status(channels: list[str]) -> list[dict]:
    """
    Devuelve una lista de estados por canal, asegurando que todos los canales del config
    aparezcan aunque no tengan estado previo.
    """
    data = load_status()
    items = []
    for ch in channels:
        items.append(
            data.get(
                ch,
                {
                    "channel": ch,
                    "status": "unknown",
                    "last_run": None,
                    "new_messages": 0,
                    "total_messages": 0,
                    "last_error": "",
                },
            )
        )
    return items