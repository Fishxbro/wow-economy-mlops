
import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "price",
    "prev_price",
    "prev2_price",
    "change_1",
    "change_2",
    "rolling_mean_3",
    "rolling_std_3",
    "quantity",
    "auctions",
    "itemid_num"
]


def build_features(history):

    history = history.sort_values("scan-time")

    current = history.iloc[-1]

    previous = (
        history.iloc[-2]
        if len(history) >= 2 else current
    )

    previous2 = (
        history.iloc[-3]
        if len(history) >= 3 else previous
    )

    price = float(current["price"])
    prev_price = float(previous["price"])
    prev2_price = float(previous2["price"])

    change_1 = (
        price / prev_price - 1
        if prev_price > 0 else 0
    )

    change_2 = (
        prev_price / prev2_price - 1
        if prev2_price > 0 else 0
    )

    recent = history["price"].tail(3)

    values = {
        "price": price,
        "prev_price": prev_price,
        "prev2_price": prev2_price,
        "change_1": change_1,
        "change_2": change_2,
        "rolling_mean_3": recent.mean(),
        "rolling_std_3": recent.std(),
        "quantity": float(current["quantity"]),
        "auctions": float(current["auctions"]),
        "itemid_num": float(str(current["itemid"]).split(':')[0])
    }

    return pd.DataFrame(
        [[values[col] for col in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )


def create_training_dataset(prices):

    samples = []

    prices = prices.sort_values(
        ["item_key", "scan-time"]
    )

    for item_key, group in prices.groupby("item_key"):

        group = group.reset_index(drop=True)

        # Necesitamos una observación anterior
        # y una observación futura para crear una etiqueta
        for i in range(1, len(group)):

            history = group.iloc[:i]

            current_price = float(
                group.iloc[i - 1]["price"]
            )

            future_price = float(
                group.iloc[i]["price"]
            )

            if current_price <= 0 or future_price <= 0:
                continue

            variation = (
                future_price / current_price
            ) - 1

            if variation > 0.01:
                target = "SUBE"

            elif variation < -0.01:
                target = "BAJA"

            else:
                target = "ESTABLE"

            features = build_features(history)

            row = features.iloc[0].to_dict()

            row["item_key"] = item_key
            row["target_scan_time"] = float(
                group.iloc[i]["scan-time"]
            )

            row["target"] = target

            samples.append(row)

    return pd.DataFrame(samples)
