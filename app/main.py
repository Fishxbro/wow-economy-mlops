
import json
import joblib
import pandas as pd

from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.features import build_features, FEATURE_COLUMNS


ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "processed" / "prices.csv"
MODEL_PATH = ROOT / "models" / "model.joblib"
METRICS_PATH = ROOT / "models" / "metrics.json"

app = FastAPI(
    title="WoW Economy API",
    description="API de precios y predicciones de World of Warcraft",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["FRONTEND_ORIGIN"].rstrip("/")] if os.environ.get("FRONTEND_ORIGIN") else [],
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
    allow_methods=["GET"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)


def load_prices():

    if not DATA_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Los datos procesados todavía no existen."
        )

    return pd.read_csv(DATA_PATH)


def load_model():

    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="El modelo todavía no ha sido entrenado."
        )

    return joblib.load(MODEL_PATH)


@app.get("/")
def home():

    return RedirectResponse(url="/docs")


@app.get("/health")
def health():

    return {
        "status": "online",
        "service": "WoW Economy API",
        "model_available": MODEL_PATH.exists(),
        "data_available": DATA_PATH.exists()
    }


@app.get("/items")
def get_items(
    response: Response,
    search: str = Query(default="", max_length=100),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):

    prices = load_prices()

    latest = (
        prices.sort_values("scan-time")
        .groupby("item_key", as_index=False)
        .tail(1)
    )

    latest = latest[
        ["item_key", "itemid", "name", "price", "scan-time"]
    ].copy()

    if search:
        latest = latest[
            latest["name"].str.contains(
                search,
                case=False,
                na=False,
                regex=False,
            )
        ]

    response.headers["X-Total-Count"] = str(len(latest))
    latest = latest.sort_values(["name", "item_key"]).iloc[offset:offset + limit]

    return latest.to_dict(orient="records")


@app.get("/items/{item_key}/history")
def get_history(item_key: str):

    prices = load_prices()

    history = prices[
        prices["item_key"] == item_key
    ].sort_values("scan-time")

    if history.empty:
        raise HTTPException(
            status_code=404,
            detail="Objeto no encontrado."
        )

    return {
        "item_key": item_key,
        "name": history.iloc[-1]["name"],
        "history": history[
            ["scan-time", "price", "quantity", "auctions"]
        ].to_dict(orient="records")
    }


@app.get("/predict/{item_key}")
def predict_price(item_key: str):

    prices = load_prices()

    history = prices[
        prices["item_key"] == item_key
    ].sort_values("scan-time")

    if len(history) < 2:
        raise HTTPException(
            status_code=400,
            detail="El objeto necesita al menos dos observaciones."
        )

    model = load_model()

    features = build_features(history)

    probabilities = model.predict_proba(
        features[FEATURE_COLUMNS]
    )[0]

    classes = model.classes_

    probability_map = {
        str(label): float(prob)
        for label, prob in zip(classes, probabilities)
    }

    predicted = str(classes[probabilities.argmax()])

    return {
        "item_key": item_key,
        "name": str(history.iloc[-1]["name"]),
        "current_price": float(history.iloc[-1]["price"]),
        "prediction": predicted,
        "confidence": float(probabilities.max()),
        "probabilities": probability_map,
        "last_scan": float(history.iloc[-1]["scan-time"]),
        "model": "Random Forest"
    }


@app.get("/metrics")
def get_metrics():

    if not METRICS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="No existen métricas disponibles."
        )

    with open(METRICS_PATH, encoding="utf-8") as file:
        return json.load(file)
