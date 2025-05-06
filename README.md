# Cuban FX Market Analysis Dashboard

## Description
Este proyecto es una aplicación web que analiza el mercado cambiario a través de técnicas avanzadas de web scraping, análisis de datos y visualización. La aplicación recolecta, procesa y visualiza datos del mercado cambiario en tiempo real, proporcionando insights valiosos sobre tendencias y patrones del mercado.

## Características Principales
- 🔍 **Web Scraping de Redes Sociales**
  - Extracción automática de mensajes relacionados con el mercado cambiario
  - Monitoreo continuo de múltiples fuentes de datos
  - Sistema robusto de recolección de datos

- 🧹 **Procesamiento de Datos**
  - Limpieza y normalización de mensajes
  - Extracción de información relevante (precios, volúmenes, fechas)
  - Validación y control de calidad de datos

- 📊 **Análisis Estadístico**
  - Simulación de subastas Walrasianas
  - Generación de estadísticas de mercado
  - Almacenamiento eficiente de datos históricos

- 📈 **Dashboard Interactivo**
  - Series temporales de precios y volúmenes
  - Histogramas de distribución
  - Curvas de oferta y demanda
  - Modelo Oculto de Markov
  - Descomposición de Modo Empírico
  - Métricas en tiempo real del mercado

## Requisitos del Sistema
- Python 3.11+
- Docker y Docker Compose
- Conexión a Internet estable

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd cuban_fx_app
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
.\venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con las configuraciones necesarias
```

5. Iniciar con Docker:
```bash
docker-compose up -d
```

## Uso

1. Iniciar la aplicación:
```bash
python main.py
```

2. Acceder al dashboard:
- Abrir navegador web
- Visitar `http://localhost:8050`

## Estructura del Proyecto

```
cuban_fx_app/
├── app.py                  # Aplicación principal Dash
├── data_storage.py         # Gestión de almacenamiento
├── services/              # Servicios principales
│   ├── framework_scraping/  # Módulos de web scraping
│   └── framework_analytics/ # Módulos de análisis
├── callback/             # Callbacks de Dash
├── components/           # Componentes reutilizables
├── layouts/             # Layouts de la interfaz
└── assets/             # Recursos estáticos
```

## Contribución
1. Fork del repositorio
2. Crear rama para feature: `git checkout -b feature/nueva-caracteristica`
3. Commit cambios: `git commit -am 'Añadir nueva característica'`
4. Push a la rama: `git push origin feature/nueva-caracteristica`
5. Crear Pull Request

## Tecnologías Utilizadas
- Python
- Dash
- Pandas
- Numpy
- Scipy
- Plotly
- Beautiful Soup/Selenium
- SQLAlchemy
- Docker

## Licencia
[Especificar tipo de licencia]

## Contacto
[Información de contacto del mantenedor]

