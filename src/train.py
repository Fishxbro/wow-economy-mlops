import json
import joblib
import mlflow
import mlflow.sklearn

import pandas as pd

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score
)

from src.features import create_training_dataset, FEATURE_COLUMNS


ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "processed" / "prices.csv"
MODELS = ROOT / "models"

MODELS.mkdir(exist_ok=True, parents=True)

MODEL_PATH = MODELS / "model.joblib"


def train():

    prices = pd.read_csv(DATA)

    dataset = create_training_dataset(prices)

    if len(dataset) < 50:
        raise ValueError(
            "No existen suficientes muestras para entrenar."
        )

    # Separación temporal: no mezclamos el futuro
    # con las observaciones del pasado.
    cutoff = dataset["target_scan_time"].quantile(0.80)

    train_data = dataset[
        dataset["target_scan_time"] <= cutoff
    ]

    test_data = dataset[
        dataset["target_scan_time"] > cutoff
    ]

    if len(train_data) < 30 or len(test_data) < 5:
        raise ValueError(
            "No hay suficientes datos para una evaluación temporal."
        )

    X_train = train_data[FEATURE_COLUMNS]
    y_train = train_data["target"]

    X_test = test_data[FEATURE_COLUMNS]
    y_test = test_data["target"]

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    )

    mlflow.set_experiment("WoW-Economy-Predictions")

    with mlflow.start_run():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        f1 = f1_score(
            y_test,
            predictions,
            average="macro"
        )

        report = classification_report(
            y_test,
            predictions,
            output_dict=True,
            zero_division=0
        )

        # Registrar parámetros
        mlflow.log_param("algorithm", "RandomForest")
        mlflow.log_param("estimators", 300)
        mlflow.log_param("max_depth", 12)
        mlflow.log_param("train_samples", len(train_data))
        mlflow.log_param("test_samples", len(test_data))
        mlflow.log_param("temporal_cutoff", float(cutoff))

        # Registrar métricas
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_macro", f1)

        # Guardar modelo
        joblib.dump(model, MODEL_PATH)

        mlflow.sklearn.log_model(
            model,
            artifact_path="wow-price-model",
            skops_trusted_types=["sklearn.tree._tree.Tree"]
        )

        metrics = {
            "accuracy": float(accuracy),
            "f1_macro": float(f1),
            "train_samples": len(train_data),
            "test_samples": len(test_data),
            "classification_report": report
        }

        with open(
            MODELS / "metrics.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metrics,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nENTRENAMIENTO COMPLETADO")
        print("-------------------------")
        print("Accuracy:", accuracy)
        print("F1 Macro:", f1)
        print("\nReporte:")
        print(classification_report(
            y_test,
            predictions,
            zero_division=0
        ))

        print("\nModelo guardado:", MODEL_PATH)


if __name__ == "__main__":
    train()