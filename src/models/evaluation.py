"""Shared confusion-matrix plotting and metric reporting.

The original notebook repeated this block for every model and split. It is
factored out here so each model module calls one function.
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score


def plot_confusion_matrix(cm, title="Confusion matrix"):
    """Plot a 2x2 confusion matrix with annotated counts."""
    plt.figure(figsize=(6.5, 6.5))
    plt.imshow(cm, interpolation="nearest", cmap="Pastel1")
    plt.title(title, size=11)
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ["false", "true"], size="x-large")
    plt.yticks(tick_marks, ["false", "true"], size="x-large")
    plt.tight_layout()
    plt.ylabel("Actual label", size=15)
    plt.xlabel("Predicted label", size=15)

    for x in range(cm.shape[0]):
        for y in range(cm.shape[1]):
            plt.annotate(str(cm[x][y]), xy=(y, x),
                         horizontalalignment="center",
                         verticalalignment="center",
                         size="x-large")


def report_performance(model, y_true, prediction, X_cv, y_cv, title="Confusion matrix"):
    """Plot the confusion matrix and print classification + regression metrics."""
    confusion = metrics.confusion_matrix(y_true, prediction)
    plt.figure()
    plot_confusion_matrix(confusion, title=title)
    plt.show()

    tn, fp, fn, tp = confusion.ravel()

    print("True Positive (TP): ", tp)
    print("True Negative (TN): ", tn)
    print("False Positive (FP): ", fp)
    print("False Negative (FN): ", fn)

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * (precision * recall) / (precision + recall)

    print("\n\nMetrics:")
    print("Accuracy: ", round(accuracy, 2))
    print("Precision: ", round(precision, 2))
    print("Recall: ", round(recall, 2))
    print("F1-score: ", round(f1_score, 2))

    rmse = np.sqrt(mean_squared_error(y_true, prediction))
    print(f"RMSE Value : {rmse:.2f}")
    print(f"R2 Score value : {r2_score(y_true, prediction):.2f}")

    # Cross validation
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    n_scores = cross_val_score(
        model, X_cv, y_cv, scoring="accuracy", cv=cv, n_jobs=-1, error_score="raise")
    print(f"Cross Validation Score: {np.mean(n_scores):.3f} ({np.std(n_scores):.3f})")
