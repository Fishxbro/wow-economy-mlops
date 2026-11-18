# Azeroth — WoW Economy MLOps

Proyecto de Machine Learning y MLOps para consultar información histórica de la economía de World of Warcraft y realizar predicciones sobre las variaciones de precio de sus objetos.

## ¿Qué hace la aplicación?

Azeroth permite:

- Buscar objetos de World of Warcraft.
- Consultar precios históricos por unidad.
- Observar variaciones entre escaneos del mercado.
- Visualizar gráficas de precios.
- Consultar las predicciones disponibles del modelo de Machine Learning.
- Marcar objetos como favoritos en la interfaz.

**Nota:** los precios proceden del conjunto de datos histórico utilizado en el proyecto. No representan necesariamente precios actuales del juego ni ventas completadas.

## Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Procesamiento de datos |
| Pandas y scikit-learn | Preparación y entrenamiento |
| MLflow | Seguimiento de experimentos |
| DVC | Versionado de datasets y modelos |
| FastAPI | API REST |
| Vue 3 y Vite | Interfaz web |
| Vue Router y Vuex | Navegación y gestión del estado |
| Apache Airflow | Orquestación de tareas |
| Docker | Ejecución de Airflow |
| Git y GitHub | Control de versiones |

## Requisitos

- Windows con WSL y Ubuntu, o un entorno Linux equivalente.
- Python y las dependencias del proyecto.
- Node.js 24.15.0 mediante nvm.
- Datasets y modelo entrenado disponibles localmente.
- Docker Desktop, únicamente para ejecutar Airflow.

## Cómo iniciar la página

### 1. Iniciar el backend

Abrir una terminal WSL:

```bash
cd ~/proyectos/wow-economy-mlops
source .venv/bin/activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verificar en:

http://localhost:8000/docs

### 2. Iniciar el frontend

Abrir otra terminal WSL:

```bash
cd ~/proyectos/wow-economy-mlops/frontend
nvm use
npm run dev
```

Abrir en el navegador la dirección que indique Vite, normalmente:

http://localhost:5173

El archivo local `frontend/.env.local` debe contener:

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

### 3. Opcional: iniciar Apache Airflow

```bash
cd ~/proyectos/wow-economy-mlops/airflow
docker compose up -d
```

Interfaz de Airflow:

http://localhost:8080

El DAG de comprobación demuestra la ejecución y supervisión de tareas. La automatización integral del entrenamiento está pendiente de implementación.

## Endpoints de FastAPI

- `/health`: comprobar el estado de la API.
- `/items`: consultar objetos.
- `/items/{item_key}/history`: consultar historial de precios.
- `/predict/{item_key}`: consultar predicciones.
- `/metrics`: consultar métricas.

## Datos y modelos

Los archivos grandes se administran mediante DVC y no se incluyen directamente en GitHub.

Para ejecutar el backend desde una instalación nueva, es necesario disponer de los datasets y del modelo entrenado. Actualmente se conservan en el entorno local de desarrollo.

## Presentación del proyecto

1. Iniciar FastAPI.
2. Iniciar Vue/Vite.
3. Abrir Azeroth en el navegador.
4. Buscar un objeto, por ejemplo, *Linen Cloth*.
5. Mostrar el precio, la variación y la gráfica histórica.
6. Mostrar las funciones de predicción disponibles.
7. Explicar cómo FastAPI consulta los datos y utiliza el modelo de Machine Learning.

## Estado

Aplicación web y backend integrados y probados en el entorno de desarrollo local. DVC y MLflow utilizados para gestión de datos y experimentos; Apache Airflow dispone de un DAG de verificación funcional.