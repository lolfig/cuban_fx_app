# Usa una imagen base con Python
FROM python:3.12.3

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone un puerto (si es necesario, por ejemplo, para una app web)
EXPOSE 5000

# Define el comando por defecto al iniciar el contenedor
CMD ["python", "app.py"]
