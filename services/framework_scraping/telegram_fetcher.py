from datetime import datetime, timezone
from typing import List
import json
from services.framework_scraping.tools.types import MessagesStep
from services.framework_scraping.tools.telegram_scrap.telegram_scrap import scrape_telegram, nombre_archivo_json
from config.settings import load_config

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
    
    # Execute the scraper
    await scrape_telegram(channels, '')
    
    # Read the messages from the JSON file
    with open(nombre_archivo_json, 'r', encoding='utf-8') as f:
        raw_messages = json.load(f)
    
    # Filter messages within the date range
    filtered_messages = [
        msg['Contenido'] 
        for msg in raw_messages 
        if start_moment <= datetime.strptime(msg['Fecha'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc) <= end_moment
    ]

    return MessagesStep(
        start=start_moment.strftime('%Y-%m-%d'),
        end=end_moment.strftime('%Y-%m-%d'),
        messages=filtered_messages
    )