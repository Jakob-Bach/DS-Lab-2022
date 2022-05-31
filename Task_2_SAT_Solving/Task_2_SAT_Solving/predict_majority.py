"""Predict majority for SAT-solving data

Script that creates a simple baseline for the SAT-solving data by predicting the majority class.
"""


import pathlib

import pandas as pd
import sklearn.dummy


DATA_DIR = pathlib.Path('data/')
TARGET = 'family'  # "family" or "result"


if __name__ == '__main__':
    X_test = pd.read_csv(DATA_DIR / f'{TARGET}_X_test.csv')
    y_train = pd.read_csv(DATA_DIR / f'{TARGET}_y_train.csv')

    model = sklearn.dummy.DummyClassifier(strategy='most_frequent')
    model.fit(X=None, y=y_train[TARGET])
    y_test_pred = model.predict(X=X_test)
    y_test_pred = pd.DataFrame({'hash': X_test['hash'], TARGET: y_test_pred})

    y_test_pred.to_csv(DATA_DIR / f'{TARGET}_predict-majority_prediction.csv', index=False)
