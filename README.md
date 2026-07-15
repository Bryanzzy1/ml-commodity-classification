# A Dynamic Framework: Advancing Machine Learning in Commodity Import Decision-Making

Code behind the paper [A Dynamic Framework: Advancing Machine Learning in Commodity Import Decision-Making](https://ieeexplore.ieee.org/document/10387664),
published at the 2023 Fifth International Conference on Transdisciplinary AI (TransAI).

The paper proposes a machine learning approach to two linked import decisions:
whether to import a given commodity, and what quantity to import. This repository
holds the pipeline behind it. The code was originally written in Google Colab as
a single notebook and was recently refactored into this repository structure.

## How the code works

1. **Load and clean** the yearly product data (`data_preprocessing.py`): read the
   Excel workbooks, drop inactive rows and rows with no prior-year reference,
   clean the column names, and concatenate every year into one frame.
2. **Score priority** (`priority_system.py`): rate each product on months of
   supply, ABC ranking, quantity and sales growth, excess inventory cost, IGMROI,
   gross margin, and COGS. The factors sum to a total priority value, and a
   product scoring above the threshold gets a buy label (`buy = 1`).
3. **Train the models** (`models/`): fit Logistic Regression, CatBoost, XGBoost,
   and AutoGluon on the buy decision. AutoGluon is also used to predict the
   optimal buy quantity. Each model is evaluated with a confusion matrix and the
   standard classification / regression metrics.

## Repository structure

```
src/
  config.py               # source sheets, column rename map, feature lists
  data_preprocessing.py   # load Excel, clean columns, combine years
  priority_system.py      # priority scoring -> total priority -> buy label
  models/
    data_split.py         # feature/target build + train/valid/test split
    evaluation.py         # confusion matrix plot + metric reporting
    logistic.py           # C sweep, train, predict
    catboost_model.py
    xgboost_model.py
    autogluon_model.py    # buy-quantity regression
notebooks/
  commodity_classification.ipynb   # orchestration, imports from src/
data/
  raw/                    # place yearly workbooks here (not tracked)
  processed/
```

## Usage

```bash
pip install -r requirements.txt
```

Place the yearly workbooks in `data/raw/`, then run
`notebooks/commodity_classification.ipynb` from the repo root. The data set is
confidential and is not included.
