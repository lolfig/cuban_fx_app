# Importaciones iniciales
import os
import json
import random
import asyncio
import builtins
import time
from datetime import datetime, timezone
from telethon.sync import TelegramClient
from config.settings import load_config
from config.telegram_status import update_channel_status

# Cargar configuración
config = load_config()
username = config['username']
phone = config['phone']
api_id = config['api_id']
api_hash = config['api_hash']
import pickle
import pandas as pd
# Configuración global
fecha_actual = datetime.now()
inicio_del_dia = datetime.combine(fecha_actual.date(), datetime.min.time()).replace(tzinfo=timezone.utc)
ruta_base = os.path.join(os.path.dirname(__file__), "Data_Scrap")
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), 
    "data", 
    "messages"
)
print(f"Buscando mensajes desde: {inicio_del_dia}")
print(f"Ruta de la carpeta 'Data_Scrap': {ruta_base}")

# Variables
nombre_archivo_json = 'mensajes.json'
clave_busqueda = ''  # Dejar vacío si no buscas palabra clave
max_reintentos = 3
# Asegura que exista el archivo JSON principal
if not os.path.exists(nombre_archivo_json):
    with open(nombre_archivo_json, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)

# Función para obtener el @ del autor
async def obtener_username(client, sender_id):
    try:
        user = await client.get_entity(sender_id)
        return user.username if user.username else "Desconocido"
    except Exception as e:
        print(f"Error al obtener el username: {e}")
        return "Desconocido"

# Función para guardar mensajes en archivos por día
def guardar_mensajes_por_dia(grupo, mensajes):
    if not mensajes:
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    mensajes_por_dia = {}
    for mensaje in mensajes:
        fecha = mensaje['Fecha'].split()[0]
        if fecha not in mensajes_por_dia:
            mensajes_por_dia[fecha] = []
        mensajes_por_dia[fecha].append(mensaje)

    for fecha, mensajes_dia in mensajes_por_dia.items():
        # Create DataFrame from messages
        df = pd.DataFrame(mensajes_dia)
        
        # Save as parquet with telegram suffix
        nombre_archivo = os.path.join(DATA_DIR, f"{fecha}_telegram.parquet")
        df.to_parquet(nombre_archivo)
        print(f"Guardado archivo: {nombre_archivo}")

# Raspado principal
async def scrape_telegram(channels, session_file):
    with open(nombre_archivo_json, 'r', encoding='utf-8') as f:
        mensajes_existentes = json.load(f)

    index = len(mensajes_existentes)
    start_time = time.time()

    async with TelegramClient(username, api_id, api_hash) as client:
        for canal in channels: # Cambiado de 'canales' a 'channels'
            reintento = 0
            mensajes_nuevos = []

            while reintento <= max_reintentos:
                try:
                    print(f"Capturando el canal: {canal}")
                    async for message in client.iter_messages(canal, search=clave_busqueda):
                        # Filtrar mensajes que están fuera del rango de la fecha
                        if message.date.replace(tzinfo=timezone.utc) < inicio_del_dia:
                            print(f"Mensaje ignorado (fuera del rango): {message.date}")
                            break

                        # Obtenemos el username del autor
                        username_autor = await obtener_username(client, message.sender_id)

                        # Guardamos el mensaje, incluso si es repetido
                        contenido = {
                            'Scraping ID': f'#ID{index:05}',
                            'Grupo': canal,
                            'Username Autor': username_autor,
                            'Contenido': message.text,
                            'Fecha': message.date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                        }
                        mensajes_nuevos.append(contenido)
                        print(f"Elemento {index:05} completado! Id: {message.id:05}.")
                        index += 1

                        await asyncio.sleep(0)  # Yield control (mejor que time.sleep)

                    # Si todo salió bien, guardamos los mensajes de este canal
                    mensajes_existentes.extend(mensajes_nuevos)
                    with open(nombre_archivo_json, 'w', encoding='utf-8') as f:
                        json.dump(mensajes_existentes, f, ensure_ascii=False, indent=4)

                    guardar_mensajes_por_dia(canal, mensajes_nuevos)
                    print(f"Total mensajes capturados en {canal}: {len(mensajes_nuevos)}\n")
                    
                    # Actualizar estado del canal en archivo JSON (éxito)
                    update_channel_status(
                        canal,
                        status="ok",
                        new_messages=len(mensajes_nuevos),
                        total_messages=len(mensajes_existentes),
                        last_error=""
                    )
                    break  # Terminó bien, salimos del bucle de reintento

                except Exception as e:
                    print(f"Error general en canal {canal}: {e}")
                    reintento += 1
                    if reintento > max_reintentos:
                        print(f"Máximo número de reintentos alcanzado para {canal}. Saltando...")
                        # Actualizar estado del canal en archivo JSON (fallo final)
                        update_channel_status(
                            canal,
                            status="error",
                            new_messages=0,
                            total_messages=len(mensajes_existentes),
                            last_error=str(e)
                        )
                    else:
                        print(f"Reintentando {canal} ({reintento}/{max_reintentos})...")
                    await asyncio.sleep(5)

    elapsed_time = time.time() - start_time
    print(f'----------------------------------------')
    print(f'#Concluido! {index} publicaciones fueron capturadas en total!')
    print(f'Tiempo total transcurrido: {elapsed_time:.2f} segundos')
    print(f'----------------------------------------\n\n\n\n')

# Función principal
# def main():
#     canales = [
#         'https://t.me/compra_venta_mlc_cu/',
#         'https://t.me/CriptoIntercambio_Cuba/',
#         # Agrega más canales si quieres
#     ]
#     asyncio.run(scrape_telegram(canales, clave_busqueda))

# if __name__ == "__main__":
#     main()
