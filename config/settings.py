import json
import os

CONFIG_FILE = 'config/telegram_config.json'

DEFAULT_CONFIG = {
    'api_id': '',
    'api_hash': '',
    'phone': '',
    'username': '',
    'channels': [],
    'update_interval': 5,
    'history_days': 30,
    'daily_run_time': '',  # opcional, formato "HH:MM", vacío si no se usa
    'lock_timeout_sec': None  # opcional: None => espera indefinida; número => segundos de espera máximo
}

def load_config():
    # Si existe, cargar y asegurar claves mínimas; si no existe o está corrupto, crear con DEFAULT_CONFIG
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
        except Exception:
            data = {}
        merged = {**DEFAULT_CONFIG, **(data or {})}
        # Si faltaban claves o hubo error, reescribimos el archivo ya normalizado
        if data != merged:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(merged, f, indent=4)
        return merged
    else:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)