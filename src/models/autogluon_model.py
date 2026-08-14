"""AutoGluon Tabular regression for the recommended buy quantity."""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import autogluon.core as ag
from autogluon.tabular import TabularPredictor

from ..config import FEATURE_COLUMNS


def add_quantity_targets(combined_data):
    """Derive the average monthly quantity and the recommended buy quantity."""
    combined_data = combined_data.copy()
    combined_data["average_qty_per_month"] = combined_data["qty_last_12_month"] / 12
    combined_data["qty_buy"] = np.where(
        combined_data["buy"] == 1,
        combined_data["average_qty_per_month"] * (combined_data["total_priority"] / 10),
        0)
    combined_data["empty"] = np.where(combined_data["buy"] == 2, 0, 1)
    return combined_data


def split_for_quantity(combined_data, random_state=15):
    """Build the feature/target frames and the train/valid/test splits."""
    predict_cols = list(FEATURE_COLUMNS) + ["buy", "average_qty_per_month", "qty_buy"]
    X = combined_data[predict_cols]
    y = combined_data[["empty"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.8, test_size=0.2, random_state=random_state)
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train, y_train, train_size=0.9, test_size=0.1, random_state=random_state)
    return X_train, X_valid, X_test, y_train, y_valid, y_test


def _hyperparameters():
    """Return the GBM hyperparameter search space and tuning arguments."""
    gbm_options = {
        "num_boost_round": 100,
        "num_leaves": ag.space.Int(lower=26, upper=66, default=36),
    }
    hyperparameters = {"GBM": gbm_options}
    hyperparameter_tune_kwargs = {
        "num_trials": 5,
        "scheduler": "local",
        "searcher": "auto",
    }
    return hyperparameters, hyperparameter_tune_kwargs


def train(X_train, X_valid, time_limit=2 * 60):
    """Fit a TabularPredictor to estimate qty_buy."""
    hyperparameters, hyperparameter_tune_kwargs = _hyperparameters()
    predictor_qty = TabularPredictor(label="qty_buy").fit(
        X_train, tuning_data=X_valid, time_limit=time_limit,
        hyperparameters=hyperparameters, hyperparameter_tune_kwargs=hyperparameter_tune_kwargs,
    )
    return predictor_qty


def error_report(predictor_qty, X_test, y_actual_qty):
    """Compare predicted qty_buy against actuals and print the mean absolute error."""
    y_test_nolabel = X_test.drop(columns="qty_buy")
    y_predict = predictor_qty.predict(y_test_nolabel).to_frame().reset_index()

    y_show = pd.DataFrame()
    y_show["qty_buy"] = y_predict["qty_buy"]
    y_show["qty_buy_actual"] = y_actual_qty.reset_index()["qty_buy"]
    y_show["difference"] = (y_show["qty_buy"] - y_show["qty_buy_actual"]).abs()
    accuracy_spec = y_show["difference"].sum() / len(y_show.index)
    print("The average range of error of the estimates was", accuracy_spec)
    return y_show
