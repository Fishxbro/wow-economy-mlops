"""Download the three runtime artifacts from a private Hugging Face Dataset repository.

Secrets come from Render environment variables. Source CSV files used to train
are NOT needed for serving the existing model.
"""
import os
from pathlib import Path
from huggingface_hub import hf_hub_download

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "data/processed/prices.csv",
    "models/model.joblib",
    "models/metrics.json",
]


def main():
    repo_id = os.getenv("HF_REPO_ID")
    token = os.getenv("HF_TOKEN")
    if not repo_id or not token:
        raise SystemExit("Faltan HF_REPO_ID o HF_TOKEN en las variables de entorno de Render")
    for path in REQUIRED_FILES:
        destination = ROOT / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        print(f"Descargando {path} desde el repositorio privado...")
        hf_hub_download(
            repo_id=repo_id,
            filename=path,
            repo_type="dataset",
            local_dir=str(ROOT),
            token=token,
        )
        if not destination.is_file() or destination.stat().st_size == 0:
            raise RuntimeError(f"No se descargó correctamente: {path}")
        print(f"OK: {path} ({destination.stat().st_size:,} bytes)")
    print("Artefactos listos para FastAPI")


if __name__ == "__main__":
    main()
