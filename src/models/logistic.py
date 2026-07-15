"""Logistic Regression: C-parameter sweep, training, and evaluation."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss


def sweep_c(X_train, y_train, X_test, y_test, num=20):
    """Scan a geometric range of C values, recording accuracy and log loss."""
    C_list = np.geomspace(1e-5, 1e5, num=num)
    CA = []
    logarithimic_loss = []

    for c in C_list:
        log_reg = LogisticRegression(random_state=10, solver="lbfgs", C=c)
        log_reg.fit(X_train, y_train)
        score = log_reg.score(X_test, y_test)
        CA.append(score)
        print("CA of c param {} is {}".format(c, score))
        pred_proba_t = log_reg.predict(X_test)
        log_loss2 = log_loss(y_test, pred_proba_t)
        logarithimic_loss.append(log_loss2)
        print("Log Loss of C param {} is {}".format(c, log_loss2))
        print("")

    outcomes = zip(C_list, np.array(CA).reshape(num,), np.array(logarithimic_loss).reshape(num,))
    df_outcome = pd.DataFrame(outcomes, columns=["C_list", "CA2", "Logarithimic_loss2"])
    return df_outcome


def best_c(df_outcome):
    """Return the C value with the highest classification accuracy."""
    c_row_max = df_outcome["CA2"].idxmax()
    return df_outcome.loc[c_row_max, "C_list"]


def train(X_train, y_train, c_val):
    """Fit the final balanced Logistic Regression at the chosen C."""
    logistic_regr = LogisticRegression(
        C=c_val, penalty="l2", solver="lbfgs", class_weight="balanced", max_iter=1000)
    logistic_regr.fit(X_train, y_train.values.ravel())
    return logistic_regr


def summarize_predictions(model, X_test, y_test):
    """Print test accuracy and the count of correct predictions."""
    prediction = model.predict(X_test)

    predict = pd.DataFrame(prediction, columns=["Prediction"])
    predict["Actual"] = y_test.reset_index()["buy"]
    predict["Count"] = np.where(predict["Prediction"] == predict["Actual"], 1, 0)
    total_count = predict["Count"].sum()

    print("Test Acc:", model.score(X_test, y_test))
    print("The number of correct predicion is:", total_count)
    return prediction
