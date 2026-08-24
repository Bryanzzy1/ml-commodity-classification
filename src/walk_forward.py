"""Leak-free walk-forward eval: forward label + expanding window with a purged seam.

Needs a `period` column (yyMM). Add `df["period"] = sheet` in load_year first.
"""

import pandas as pd

from .config import FEATURE_COLUMNS

# abc_class carries the old rule's priority_ranking summand; drop it.
WF_FEATURES = [c for c in FEATURE_COLUMNS if c != "abc_class"]


def add_forward_label(df, horizon=1):
    """Label period t from period t+horizon actuals, per product."""
    df = df.sort_values(["product_id", "period"]).copy()
    df["_future"] = df.groupby("product_id")["qty_last_12_month"].shift(-horizon)
    df = df.dropna(subset=["_future"])
    df["label"] = (df["_future"] > df["qty_last_12_month"]).astype(int)
    return df.drop(columns="_future")


def walk_forward_purged(df, horizon=1, min_train=1, embargo=0):
    """Expanding-window folds; purge train rows whose label matures into the test period."""
    periods = sorted(df["period"].unique())
    idx = df["period"].map({p: i for i, p in enumerate(periods)})
    for k in range(min_train, len(periods)):
        train = df[(idx < k - embargo) & (idx + horizon < k)]  # time order + purge
        test = df[idx == k]
        if not train.empty and not test.empty:
            yield train, test


if __name__ == "__main__":
    # Purge must drop the seam: no train label may mature on/after its fold's test period.
    rows = [{"product_id": p, "period": f"20{i:02d}", "qty_last_12_month": i}
            for p in "abc" for i in range(6)]
    df = add_forward_label(pd.DataFrame(rows))
    order = {p: i for i, p in enumerate(sorted(df["period"].unique()))}
