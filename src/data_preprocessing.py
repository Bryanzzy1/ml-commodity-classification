"""Load yearly Excel workbooks, clean columns, and combine into one dataset."""

import pandas as pd

from .config import (
    COGS_ZERO_COLUMNS,
    COLUMN_RENAME,
    SELECTED_COLUMNS,
    YEAR_FILES,
)


def _clean_columns(df):
    """Drop duplicate columns and apply the snake_case rename map."""
    df = df.loc[:, ~df.columns.duplicated()].copy()
    # Collapse double spaces so raw headers match the rename keys.
    df.columns = [c.replace("  ", " ").strip() for c in df.columns]
    df = df.rename(columns=COLUMN_RENAME)
    return df


def load_year(data_dir, file_name, sheets):
    """Read the monthly sheets from one workbook and drop all-zero-COGS rows."""
    df = pd.concat(
        [pd.read_excel(f"{data_dir}/{file_name}", sheet_name=sheet) for sheet in sheets],
        ignore_index=True,
    )
    df = _clean_columns(df)

    # Drop rows where every COGS figure is zero (no activity).
    zero_mask = pd.Series(True, index=df.index)
    for col in COGS_ZERO_COLUMNS:
        zero_mask &= df[col].astype(str) == "0"
    df = df[~zero_mask]
    return df


def _drop_no_py(df):
    """Remove rows with no prior-year growth reference ("No PY")."""
    df = df.drop(df[df["qty_growth_pct_current_month"] == "No PY"].index)
    df = df.drop(df[df["sales_growth_pct_current_month"] == "No PY"].index)
    return df


def build_dataset(data_dir="data/raw"):
    """Load every year, clean, select columns, and concatenate into one frame."""
    frames = []
    for _, (file_name, sheets) in YEAR_FILES.items():
        df = load_year(data_dir, file_name, sheets)
        df = _drop_no_py(df)
        df = df[SELECTED_COLUMNS]
        frames.append(df)

    combined_data = pd.concat(frames, ignore_index=True)
    return combined_data
