"""Central configuration: source sheets, column renaming, and feature lists.

All column and table renaming lives here so the rest of the pipeline uses
consistent snake_case names.
"""

# Source Excel workbooks and the monthly sheets to read from each.
YEAR_FILES = {
    "data_2017": ("2017.xlsx", ["1706", "1707", "1708", "1709", "1710", "1711", "1712"]),
    "data_2018": ("2018.xlsx", ["1801", "1802", "1803", "1804", "1805", "1806",
                                "1807", "1808", "1809", "1810", "1811", "1812"]),
    "data_2019": ("2019.xlsx", ["1901", "1902", "1903", "1904", "1905", "1906",
                                "1907", "1908", "1909", "1910", "1911", "1912"]),
    "data_2020": ("2020.xlsx", ["2001", "2002", "2003"]),
}

# Raw Excel headers -> clean snake_case names.
COLUMN_RENAME = {
    "Item": "product_id",
    "Description": "product_desc",
    "ABC": "abc_class",
    "Inventory On Hand (Qty)": "inventory_on_hand_qty",
    "Months of Supply": "months_of_supply",
    "Excess Inventory Cost (> 1 year)": "excess_inventory_cost",
    "Inventory cost": "inventory_cost",
    "Inventory GMROI": "inventory_gmroi",
    "Qty Curr Month": "qty_current_month",
    "Qty YTD": "qty_ytd",
    "Qty Last 3 Month": "qty_last_3_month",
    "Qty Last 12 Month": "qty_last_12_month",
    "Qty PY YTD": "qty_py_ytd",
    "QtyPY Last 3 Month": "qty_py_last_3_month",
    "Qty PY Last 12 Month": "qty_py_last_12_month",
    "Qty PY Curr Month": "qty_py_current_month",
    "% Qty Growth Curr Month": "qty_growth_pct_current_month",
    "% Qty Growth YTD": "qty_growth_pct_ytd",
    "% Qty Growth Last 3 Month": "qty_growth_pct_last_3_month",
    "% Qty Growth Last 12 Month": "qty_growth_pct_last_12_month",
    "% Sales Growth Curr Month": "sales_growth_pct_current_month",
    "% Sales Growth YTD": "sales_growth_pct_ytd",
    "% Sales Growth Last 3 Month": "sales_growth_pct_last_3_month",
    "% Sales Growth Last 12 Month": "sales_growth_pct_last_12_month",
    "Gross Margin %": "gross_margin_pct",
    "COGS + Decorating": "cogs_plus_decorating",
    "COGS Curr Month": "cogs_current_month",
    "COGS YTD": "cogs_ytd",
    "COGS Last 3 Month": "cogs_last_3_month",
    "COGS Last 12 Month": "cogs_last_12_month",
    "COGS Curr Month PY": "cogs_current_month_py",
    "COGS YTD PY": "cogs_ytd_py",
}

# COGS columns used to drop all-zero rows on load.
COGS_ZERO_COLUMNS = [
    "cogs_current_month",
    "cogs_ytd",
    "cogs_last_3_month",
    "cogs_last_12_month",
    "cogs_current_month_py",
    "cogs_ytd_py",
]

# Columns kept after cleaning (product identifiers + base features).
SELECTED_COLUMNS = ["product_id", "product_desc"] + [
    "abc_class", "inventory_on_hand_qty", "months_of_supply", "excess_inventory_cost",
    "inventory_cost", "inventory_gmroi", "qty_current_month", "qty_ytd", "qty_last_3_month",
    "qty_last_12_month", "qty_py_ytd", "qty_py_last_3_month", "qty_py_last_12_month",
    "qty_py_current_month", "qty_growth_pct_current_month", "qty_growth_pct_ytd",
    "qty_growth_pct_last_3_month", "qty_growth_pct_last_12_month", "sales_growth_pct_current_month",
    "sales_growth_pct_ytd", "sales_growth_pct_last_3_month", "sales_growth_pct_last_12_month",
    "gross_margin_pct", "cogs_plus_decorating",
]

# Base model features (no engineered priority columns).
FEATURE_COLUMNS = [
    "abc_class", "inventory_on_hand_qty", "months_of_supply", "excess_inventory_cost",
    "inventory_cost", "inventory_gmroi", "qty_current_month", "qty_ytd", "qty_last_3_month",
    "qty_last_12_month", "qty_py_ytd", "qty_py_last_3_month", "qty_py_last_12_month",
    "qty_py_current_month", "qty_growth_pct_current_month", "qty_growth_pct_ytd",
    "qty_growth_pct_last_3_month", "qty_growth_pct_last_12_month", "sales_growth_pct_current_month",
    "sales_growth_pct_ytd", "sales_growth_pct_last_3_month", "sales_growth_pct_last_12_month",
    "gross_margin_pct", "cogs_plus_decorating",
]

# Engineered priority-system features.
PRIORITY_COLUMNS = [
    "priority_inventory", "priority_ranking", "priority_qty_percent", "priority_sale_percent",
    "priority_excess_inventory_cost", "priority_inventory_gmroi", "priority_cogs_plus_decorating",
]
