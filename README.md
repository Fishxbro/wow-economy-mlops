
# WoW Economy MLOps

Plataforma de consulta y análisis predictivo de precios
de objetos de World of Warcraft.

## Descripción

WoW Economy es un proyecto de Machine Learning y MLOps
que utiliza información histórica de subastas para
analizar el comportamiento de los precios de los objetos
de World of Warcraft.

El sistema permite consultar objetos, visualizar sus
precios históricos y obtener predicciones sobre su
posible comportamiento futuro.

## Tecnologías utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest
- MLflow
- FastAPI
- Git y GitHub

## Estructura del proyecto

```text
wow-economy-mlops/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── src/
│   ├── prepare_data.py
│   ├── features.py
│   └── train.py
│
├── app/
│   └── main.py
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.11 o compatible.
- Git.
- Entorno virtual de Python.

## Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd wow-economy-mlops
```

Crear entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Preparar los datos

Colocar los archivos originales:

- auctions.csv
- items.csv

Dentro de:

```text
data/raw/
```

Ejecutar:

```bash
python -m src.prepare_data
```

## Entrenar el modelo

```bash
python -m src.train
```

El modelo entrenado y las métricas se guardan
localmente dentro de la carpeta models/.

## MLflow

Iniciar la interfaz:

```bash
mlflow ui --host 0.0.0.0 --port 5000
```

Acceder a:

http://localhost:5000

## FastAPI

Iniciar el servidor:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Aplicación:

http://localhost:8000

Documentación:

http://localhost:8000/docs

## Endpoints principales

| Endpoint | Función |
|---|---|
| GET /health | Estado de la API |
| GET /items | Catálogo de objetos |
| GET /items/{item_key}/history | Historial de precios |
| GET /predict/{item_key} | Predicción del objeto |
| GET /metrics | Métricas del modelo |

## Estado del proyecto

En desarrollo.

Frontend y demás componentes de infraestructura
MLOps pendientes de integración.

## Autoría

Proyecto académico: WoW Economy MLOps.
