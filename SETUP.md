# Arranque local de la API

Desde la carpeta `wow-economy-mlops`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-api.txt
.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Comprueba `http://127.0.0.1:8000/health`. La ruta `/` abre la documentación en `/docs`.

El catálogo admite paginación: `GET /items?limit=5&offset=5` devuelve la segunda página de cinco objetos. El encabezado `X-Total-Count` indica cuántos objetos coinciden con la búsqueda completa.

## Datos necesarios

El repositorio contiene archivos `.dvc` que describen los datos y el modelo, pero no contiene los archivos reales. Además, `.dvc/config` no tiene un remoto configurado; por eso `dvc pull` no puede recuperarlos por sí solo.

Para activar `/items` y `/items/{item_key}/history`, consigue uno de estos recursos:

1. `data/processed/prices.csv`, ya procesado; o
2. `data/raw/items.csv` y `data/raw/auctions.csv`, y ejecuta:

```bash
.venv/bin/python -m src.prepare_data
```

El script espera estas columnas en los CSV originales:

| Archivo | Columnas requeridas |
| --- | --- |
| `items.csv` | `itemid`, `modifier`, `name`, `url` |
| `auctions.csv` | `itemid`, `modifier`, `scan-time`, `buyout`, `quantity` |

`/predict/{item_key}` requiere además `models/model.joblib`. `/metrics` requiere `models/metrics.json`. Si tienes suficientes datos procesados y quieres generar ambos, instala las dependencias completas de `requirements.txt` y ejecuta `.venv/bin/python -m src.train`.

Airflow y MLflow son opcionales para consultar el catálogo. El archivo `airflow/docker-compose.yaml` requiere su propio `airflow/.env` antes de levantar los contenedores.
