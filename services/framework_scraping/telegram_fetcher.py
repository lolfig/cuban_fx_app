from datetime import datetime, timezone
from typing import List
import json
import pandas as pd
from services.framework_scraping.data_processing import save_data_info
from services.framework_scraping.data_processing import generate_orders # Modificado
from services.framework_scraping.tools.messages import interpret
from config.const import DIR_TELEGRAM_MESSAGES
from services.framework_scraping.tools.types import MessagesStep
from services.framework_scraping.tools.telegram_scrap.telegram_scrap import scrape_telegram, nombre_archivo_json
from config.settings import load_config
from config.telegram_status import load_status # Importar load_status

async def fetch_telegram_messages(
    currency: str,
    start_moment: datetime,
    end_moment: datetime
) -> MessagesStep:
    """Bridge between your scraper and the project's pipeline"""
    
    # Load channels from config
    config = load_config()
    channels = config.get('channels', [])
    
    # Si no hay canales configurados, NO usar valores por defecto hardcodeados
    if not channels:
        return MessagesStep(
            start=start_moment.strftime('%Y-%m-%d'),
            end=end_moment.strftime('%Y-%m-%d'),
            messages=[]
        )
    
    # --- NUEVO: Filtrar canales según la última ejecución ---
    now_utc = datetime.now(timezone.utc)
    channel_statuses = load_status()
    channels_to_scrape = []

    for channel_url in channels:
        status_info = channel_statuses.get(channel_url)
        if status_info and status_info.get('last_run'):
            last_run_str = status_info['last_run']
            last_run_dt = datetime.fromisoformat(last_run_str)
            # Asegurarse de que last_run_dt también sea consciente de la zona horaria
            if last_run_dt.tzinfo is None:
                last_run_dt = last_run_dt.replace(tzinfo=timezone.utc)

            time_difference = now_utc - last_run_dt
            if time_difference.days >= 1: # Solo raspar si ha pasado al menos 1 día
                channels_to_scrape.append(channel_url)
            else:
                print(f"Saltando scraping para {channel_url}. Última ejecución fue hace menos de 1 día.")
        else:
            # Si no hay información de estado o last_run, raspar por defecto
            channels_to_scrape.append(channel_url)
    
    if not channels_to_scrape:
        print("No hay canales para raspar en este momento.")
        return MessagesStep(
            start=start_moment.strftime('%Y-%m-%d'),
            end=end_moment.strftime('%Y-%m-%d'),
            messages=[]
        )
    # --- FIN NUEVO ---

    # Espera hasta adquirir el lock antes de raspar Telegram
    from services.framework_scraping.locks import AsyncFileLock, DEFAULT_LOCK_PATH
    from config.const import SCRAPER_LOCK_TIMEOUT_SEC

    timeout = config.get('lock_timeout_sec', None)
    if timeout is None:
        timeout = SCRAPER_LOCK_TIMEOUT_SEC

    async with AsyncFileLock(DEFAULT_LOCK_PATH, poll_interval=0.5, timeout=timeout):
        # Ejecutar el scraper (actualiza mensajes.json)
        await scrape_telegram(channels_to_scrape, '') # Usar channels_to_scrape
    
    # Cargar los mensajes crudos desde el JSON
    with open(nombre_archivo_json, 'r', encoding='utf-8') as f:
        raw_messages = json.load(f)
    
    # Filtrar mensajes dentro del rango de fechas
    filtered_dicts = [
        msg
        for msg in raw_messages
        if start_moment <= datetime.strptime(msg['Fecha'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc) <= end_moment
    ]
    filtered_messages = [msg['Contenido'] for msg in filtered_dicts]

    # 1) Construir DataFrame de mensajes (igual que el pipeline)
    messages_df = pd.DataFrame(
        filtered_messages,
        columns=[end_moment.strftime('%Y-%m-%d')]
    )

    # 2) Procesar con interpret y generar formal orders
    processed_data = [interpret(m) for m in filtered_messages]
    orders = generate_orders(processed_data)

    # 3) Guardar parquet compatible en data/messages_telegram
    #    (mismo esquema: columns = [messages, processed_messages, orders])
    save_data_info(
        date=end_moment,
        messages=messages_df,
        processed_data=processed_data,
        orders=orders,
        target_dir=DIR_TELEGRAM_MESSAGES
    )

    # Devolver también para quien invoque el fetcher
    return MessagesStep(
        start=start_moment.strftime('%Y-%m-%d'),
        end=end_moment.strftime('%Y-%m-%d'),
        messages=filtered_messages
    )