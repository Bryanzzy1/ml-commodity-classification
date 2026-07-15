"""XGBoost classifier training."""

import numpy as np
from xgboost import XGBClassifier


def train_predict(X_train, y_train, X_test):
    """Fit XGBoost on numeric features and return the trained model + predictions."""
    xgb = XGBClassifier()
    prediction = xgb.fit(
        X_train._get_numeric_data(), np.ravel(y_train, order="C")
    ).predict(X_test._get_numeric_data())
    return xgb, prediction
