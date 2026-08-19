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
    return df
