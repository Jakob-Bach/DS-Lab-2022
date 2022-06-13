"""K-means clustering for SAT-solving data

Script that clusters the SAT-solving data with standard k-means.
"""


import pathlib

import pandas as pd
import sklearn.cluster


DATA_DIR = pathlib.Path('data/')
TARGET = 'family'  # "family" or "result"


if __name__ == '__main__':
    X_train = pd.read_csv(DATA_DIR / f'{TARGET}_X_train.csv')
    X_test = pd.read_csv(DATA_DIR / f'{TARGET}_X_test.csv')
    y_train = pd.read_csv(DATA_DIR / f'{TARGET}_y_train.csv')

    model = sklearn.cluster.KMeans(n_clusters=y_train[TARGET].nunique(), random_state=25)
    # fit() + separate predict() (cluster assignment) doesn't work for all sklearn clustering algos;
    # alternatively, one could directly cluster the test data, or cluster train + test together
    model.fit(X=X_train.drop(columns='hash'))
    y_test_pred = model.predict(X=X_test.drop(columns='hash'))
    y_test_pred = pd.DataFrame({'hash': X_test['hash'], TARGET: y_test_pred})

    y_test_pred.to_csv(DATA_DIR / f'{TARGET}_cluster-k-means_prediction.csv', index=False)
