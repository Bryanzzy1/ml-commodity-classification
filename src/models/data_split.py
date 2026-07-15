"""Train/validation/test splitting shared by the classifier models."""

from sklearn.model_selection import train_test_split

from ..config import FEATURE_COLUMNS, PRIORITY_COLUMNS


def make_xy(combined_data, use_priority_features=False):
    """Build the feature matrix X and target y (buy).

    ABC class is replaced by its numeric priority ranking. When
    use_priority_features is True the engineered priority columns are appended.
    """
    combined_data = combined_data.copy()
    combined_data["abc_class"] = combined_data["priority_ranking"]

    feature_cols = list(FEATURE_COLUMNS)
    if use_priority_features:
        feature_cols = feature_cols + list(PRIORITY_COLUMNS)

    X = combined_data[feature_cols]
    y = combined_data[["buy"]]
    return X, y


def split_train_valid_test(X, y, random_state=42):
    """80/20 train/test, then carve 10% of train into a validation set."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.8, test_size=0.2, random_state=random_state)
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train, y_train, train_size=0.9, test_size=0.1, random_state=random_state)
    return X_train, X_valid, X_test, y_train, y_valid, y_test
