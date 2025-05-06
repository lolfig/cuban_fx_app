# Aplicación Cuban FX - Documentación del Proyecto

## Descripción General del Proyecto
Esta es una aplicación web construida con FastAPI y Dash que monitorea y analiza las tasas de cambio de divisas cubanas. La aplicación cuenta con sincronización de datos en tiempo real, visualizaciones interactivas y un panel de control para análisis de datos.

## Estructura de Directorios

### 📁 Directorio Raíz

#### Archivos Principales
- `main.py` - Punto de entrada de la aplicación
- `app.py` - Configuración e inicialización principal de la aplicación
- `data_storage.py` - Sistema central de gestión de datos
- `requirements.txt` - Dependencias del proyecto
- `Dockerfile` & `docker-compose.yml` - Configuración de contenedores

### 📁 /assets
- `style.css` - Estilos globales para la aplicación

### 📁 /callback
Gestión de manejadores de eventos y componentes reactivos
- `/page_dashboard/` - Callbacks de la página del panel de control
- `/page_data_status/` - Callbacks de la página de estado de datos
- `/storages/` - Callbacks de gestión de almacenamiento de datos
- `websocket.py` - Manejadores de eventos WebSocket
- `navigation_drawer.py` - Callbacks del menú de navegación

### 📁 /components
Componentes de UI reutilizables
- `cards.py` - Definiciones de componentes de tarjetas
- `github_cmp.py` - Componente de visualización estilo GitHub
- `tables.py` - Definiciones de componentes de tablas
- `tools.py` - Funciones utilitarias para componentes

### 📁 /config
Gestión de configuración
- `const.py` - Constantes globales
- Configuraciones de entorno

### 📁 /layouts
Diseños de página y estructura de UI
- `/page_dashboard/` - Diseño del panel de control principal
  - Indicadores de progreso
  - Visualizaciones de datos
  - Paneles de control
- `/page_data_status/` - Diseño de la página de estado de datos
  - Controles de carga/descarga
  - Estado de sincronización
  - Indicadores de progreso

### 📁 /reactivity
Gestión de estado y componentes reactivos
- `/storage/` - Definiciones de almacenamiento de datos
  - `background_task.py` - Estado de tareas en segundo plano
  - `background_task_progress.py` - Seguimiento de progreso
  - `missing_data_counter.py` - Monitoreo de datos faltantes
  - `global_state.py` - Estado global de la aplicación

### 📁 /routes
Gestión de rutas URL y páginas

### 📁 /services
Lógica de negocio principal y servicios externos
- `/framework_scraping/` - Funcionalidad de extracción de datos
  - `time_series_fetcher.py` - Obtención de datos de divisas
  - Herramientas para gestionar fechas faltantes

### 📁 /tasks
Gestión de tareas en segundo plano
- Colas de tareas
- Gestores de sincronización
- Trabajos de procesamiento de datos

## Características Principales

### 1. Sincronización de Datos
- Obtención de datos en tiempo real de fuentes externas
- Seguimiento de progreso y actualizaciones de estado
- Gestión de tareas en segundo plano

### 2. Panel de Control Interactivo
- Visualizaciones de tasas de cambio de divisas
- Análisis de datos históricos
- Gráficos de oferta y demanda
- Sistema de seguimiento de mensajes

### 3. Gestión de Datos
- Almacenamiento de archivos Parquet
- Funcionalidad de carga/descarga
- Detección y manejo de datos faltantes

### 4. Integración WebSocket
- Actualizaciones en tiempo real
- Comunicación cliente-servidor
- Arquitectura basada en eventos

## Interacciones entre Componentes

### Flujo de Datos
1. Los datos externos se obtienen a través de `services/framework_scraping`
2. Los datos se procesan y almacenan usando `data_storage.py`
3. Los componentes de UI en `/layouts` muestran los datos
4. Los manejadores `/callback` gestionan las interacciones del usuario
5. `/reactivity` gestiona los cambios de estado

### Gestión de Estado
- Estado global manejado a través de `reactivity/storage`
- Tareas en segundo plano monitoreadas via `storage_background_task`
- Seguimiento de progreso a través de `storage_background_task_progress`

### Interfaz de Usuario
- Componentes modulares en `/components`
- Diseños de página en `/layouts`
- Elementos interactivos gestionados por `/callback`

## Despliegue
- Contenedorización Docker disponible
- Configuraciones específicas por entorno
- Arquitectura escalable

## Pautas de Desarrollo
1. Usar componentes de Storage para salidas compartidas
2. Implementar callbacks para interacciones de UI
3. Mantener estructura modular de componentes
4. Seguir convenciones de nomenclatura establecidas

## Integración de API
- Comunicación API externa a través de `services`
- Implementación WebSocket para actualizaciones en tiempo real
- Endpoints RESTful para acceso a datos

Esta documentación proporciona una visión general de alto nivel de la estructura y componentes del proyecto. Cada módulo está diseñado para ser modular y mantenible, siguiendo las mejores prácticas para el desarrollo de aplicaciones web.
