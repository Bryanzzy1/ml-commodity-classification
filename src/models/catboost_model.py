"""CatBoost classifier training."""

from catboost import CatBoostClassifier

# ABC class and product identifier act as categorical features.
CAT_FEATURES = [0, 1]


def train(X_train, y_train, cat_features=None):
    """Fit a small CatBoost classifier (matches the notebook settings)."""
    cat_features = CAT_FEATURES if cat_features is None else cat_features
    cbr = CatBoostClassifier(iterations=2, learning_rate=1, depth=2)
    cbr.fit(X_train, y_train, cat_features)
    return cbr
