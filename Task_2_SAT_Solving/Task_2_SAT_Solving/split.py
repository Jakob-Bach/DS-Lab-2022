"""Split SAT-solving data for course-internal scoring

Script that creates and saves a stratified train-test split of the SAT instances for both targets.
"""


import pathlib

import pandas as pd
import sklearn.model_selection


DATA_DIR = pathlib.Path('data/')
SEED = 25
TARGETS = ['family', 'result']


if __name__ == '__main__':
    dataset = pd.read_csv(DATA_DIR / 'dataset.csv')
    X = dataset[[x for x in dataset.columns if not x.startswith('meta.')]]
    for target in TARGETS:
        y = dataset[['hash', f'meta.{target}']].rename(columns={f'meta.{target}': target})
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
            X, y, test_size=0.2, random_state=SEED, stratify=y[target])
        X_train.to_csv(DATA_DIR / f'{target}_X_train.csv', index=False)
        X_test.to_csv(DATA_DIR / f'{target}_X_test.csv', index=False)
        y_train.to_csv(DATA_DIR / f'{target}_y_train.csv', index=False)
        y_test.to_csv(DATA_DIR / f'{target}_y_test.csv', index=False)
