"""Priority scoring system that turns features into a buy/no-buy label."""

import numpy as np
import pandas as pd


def add_priority_scores(combined_data):
    """Compute per-rule priority scores, a total score, and the buy label.

    Mirrors the original scoring rules: inventory level, ABC ranking, quantity
    and sales growth, excess inventory cost, GMROI, gross margin, and COGS.
    """
    # Inventory
    conditions_inventory = [combined_data["months_of_supply"] <= 5]
    values_inventory = [10]

    # Ranking
    conditions_ranking = [
        combined_data["abc_class"] == "A+",
        combined_data["abc_class"] == "A",
        combined_data["abc_class"] == "B",
        combined_data["abc_class"] == "C",
    ]
    values_ranking = [3, 2, 1, -5]

    # % Qty growth
    combined_data["condition_qty_percent"] = combined_data.apply(
        lambda row: row.qty_growth_pct_current_month +
        row.qty_growth_pct_ytd +
        row.qty_growth_pct_last_3_month +
        row.qty_growth_pct_last_12_month, axis=1)
    conditions_qty_percent = [combined_data["condition_qty_percent"] / 4 > 0.50,
                              (combined_data["condition_qty_percent"] / 4 <= 0.50) & (combined_data["condition_qty_percent"] / 4 >= 0),
                              combined_data["condition_qty_percent"] / 4 < 0]
    values_qty_percent = [2, 1, -2]

    # % Sales growth
    combined_data["condition_sale_percent"] = combined_data.apply(
        lambda row: row.sales_growth_pct_current_month +
        row.sales_growth_pct_ytd +
        row.sales_growth_pct_last_3_month +
        row.sales_growth_pct_last_12_month, axis=1)
    conditions_sale_percent = [combined_data["condition_sale_percent"] / 4 > 0.50,
                               (combined_data["condition_sale_percent"] / 4 <= 0.50) & (combined_data["condition_sale_percent"] / 4 >= 0),
                               combined_data["condition_sale_percent"] / 4 < 0]
    values_sale_percent = [2, 1, -2]

    # Excess inventory
    conditions_excess_inventory_cost = [combined_data["excess_inventory_cost"] > 0,
                                        combined_data["excess_inventory_cost"] <= 0]
    values_excess_inventory_cost = [-3, 0.5]

    # Inventory GMROI
    combined_data.loc[combined_data["inventory_gmroi"] == " ", "inventory_gmroi"] = 0
    combined_data["inventory_gmroi"] = pd.to_numeric(combined_data["inventory_gmroi"])
    conditions_inventory_gmroi = [(combined_data["inventory_gmroi"]) >= 3,
                                  (combined_data["inventory_gmroi"]) >= -3,
                                  (combined_data["inventory_gmroi"] < -3)]
    values_inventory_gmroi = [1, combined_data["inventory_gmroi"] / 2, -1.5]

    # Gross Margin % feeds the total score directly (no separate priority rule).

    # COGS + Decorating cost
    conditions_cogs_plus_decorating = [combined_data["cogs_plus_decorating"] == combined_data["cogs_plus_decorating"]]
    values_cogs_plus_decorating = [combined_data["cogs_plus_decorating"] / 100]

    # Priority system create
    combined_data["priority_inventory"] = np.select(conditions_inventory, values_inventory)
    combined_data["priority_ranking"] = np.select(conditions_ranking, values_ranking)
    combined_data["priority_qty_percent"] = np.select(conditions_qty_percent, values_qty_percent)
    combined_data["priority_sale_percent"] = np.select(conditions_sale_percent, values_sale_percent)
    combined_data["priority_excess_inventory_cost"] = np.select(conditions_excess_inventory_cost, values_excess_inventory_cost)
    combined_data["priority_inventory_gmroi"] = np.select(conditions_inventory_gmroi, values_inventory_gmroi)
    combined_data["priority_cogs_plus_decorating"] = np.select(conditions_cogs_plus_decorating, values_cogs_plus_decorating)

    # Total priority system
    combined_data["total_priority"] = combined_data.apply(
        lambda row: row.priority_inventory +
        row.priority_ranking +
        row.priority_qty_percent +
        row.priority_sale_percent +
        row.priority_excess_inventory_cost +
        row.priority_inventory_gmroi +
        row.gross_margin_pct +
        row.priority_cogs_plus_decorating, axis=1)

    # Buy Decision
    combined_data["buy"] = np.where(combined_data["total_priority"] >= 10, 1, 0)
    combined_data = combined_data.dropna()
    return combined_data
