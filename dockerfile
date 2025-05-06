# Usa una imagen base con Python
FROM python:3.11.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 para uvicorn
EXPOSE 8000

# Define el comando por defecto al iniciar el contenedor
CMD ["python", "main.py"]
