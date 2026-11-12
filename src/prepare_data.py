
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)


def normalize_modifier(value):
    if pd.isna(value):
        return "base"

    return str(int(float(value)))


def prepare_data():

    auctions = pd.read_csv(
        RAW / "auctions.csv",
        dtype={"itemid": str}
    )

    items = pd.read_csv(
        RAW / "items.csv",
        dtype={"itemid": str}
    )

    # Normalizar identificadores
    auctions["itemid"] = auctions["itemid"].astype(str)
    items["itemid"] = items["itemid"].astype(str)

    auctions["modifier_key"] = auctions["modifier"].apply(
        normalize_modifier
    )

    items["modifier_key"] = items["modifier"].apply(
        normalize_modifier
    )

    auctions["item_key"] = (
        auctions["itemid"] + "_" + auctions["modifier_key"]
    )

    items["item_key"] = (
        items["itemid"] + "_" + items["modifier_key"]
    )

    # Limpiar datos numéricos
    auctions["scan-time"] = pd.to_numeric(
        auctions["scan-time"], errors="coerce"
    )

    auctions["buyout"] = pd.to_numeric(
        auctions["buyout"], errors="coerce"
    )

    auctions["quantity"] = pd.to_numeric(
        auctions["quantity"], errors="coerce"
    )

    # Solo utilizamos subastas con compra inmediata válida
    auctions = auctions[
        (auctions["buyout"] > 0) &
        (auctions["quantity"] > 0) &
        (auctions["scan-time"].notna())
    ].copy()

    # Normalizar el precio por unidad
    auctions["unit_price"] = (
        auctions["buyout"] / auctions["quantity"]
    )

    # Agrupar por objeto y escaneo
    prices = (
        auctions
        .groupby(
            ["item_key", "itemid", "modifier_key", "scan-time"],
            as_index=False
        )
        .agg(
            price=("unit_price", "median"),
            quantity=("quantity", "sum"),
            auctions=("unit_price", "count")
        )
    )

    # Evitar nombres duplicados en el catálogo
    catalog = (
        items[["item_key", "itemid", "name", "url"]]
        .drop_duplicates("item_key")
    )

    prices = prices.merge(
        catalog,
        on=["item_key", "itemid"],
        how="left"
    )

    # Recuperar el nombre por itemid cuando no exista
    # una coincidencia exacta de modificador
    fallback = (
        items.drop_duplicates("itemid")
        .set_index("itemid")["name"]
    )

    prices["name"] = prices["name"].fillna(
        prices["itemid"].map(fallback)
    )

    prices["name"] = prices["name"].fillna(
        "Objeto " + prices["itemid"]
    )

    prices = prices.sort_values(
        ["item_key", "scan-time"]
    )

    output = PROCESSED / "prices.csv"

    prices.to_csv(output, index=False)

    print("Procesamiento completado.")
    print(f"Registros: {len(prices)}")
    print(f"Objetos: {prices['item_key'].nunique()}")
    print(f"Escaneos: {prices['scan-time'].nunique()}")
    print(f"Archivo guardado: {output}")


if __name__ == "__main__":
    prepare_data()
