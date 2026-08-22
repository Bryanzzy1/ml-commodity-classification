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
