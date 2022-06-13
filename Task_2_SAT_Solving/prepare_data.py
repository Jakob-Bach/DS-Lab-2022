"""Prepare SAT-solving data

Script that prepares the dataset for the practical course by:
    - downloading necessary databases with meta data and instance features from GBD
    - merging databases
    - filter the dataset (solved instances, no NAs in instance features, no very rare families)
"""


import pathlib
import urllib

import gbd_tool.gbd_api
import pandas as pd


DATA_DIR = pathlib.Path('data/')
DATABASE_NAMES = ['base', 'gate', 'meta']


if __name__ == '__main__':
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Download and save database files:
    for db_name in DATABASE_NAMES:
        urllib.request.urlretrieve(url=f'https://gbd.iti.kit.edu/getdatabase/{db_name}_db',
                                   filename=DATA_DIR / f'{db_name}.db')
        with gbd_tool.gbd_api.GBD(db_list=[str(DATA_DIR / f'{db_name}.db')]) as api:
            features = api.get_features()
            features.remove('hash')  # will be added to result anyway, so avoid duplicates
            database = pd.DataFrame(api.query_search(resolve=features), columns=['hash'] + features)
            database.to_csv(DATA_DIR / f'{db_name}.csv', index=False)

    # Merge database files:
    dataset = pd.read_csv(DATA_DIR / 'meta.csv')
    dataset.rename(columns=lambda x: f'meta.{x}' if x != 'hash' else x, inplace=True)
    numeric_cols = []
    for db_name in DATABASE_NAMES:
        if db_name != 'meta':
            database = pd.read_csv(DATA_DIR / (db_name + '.csv'))
            database.rename(columns=lambda x: f'{db_name}.{x}' if x != 'hash' else x, inplace=True)
            numeric_cols.extend([x for x in database.columns if x != 'hash'])
            dataset = dataset.merge(database, on='hash', how='left', copy=False)

    # Pre-process dataset:
    dataset[numeric_cols] = dataset[numeric_cols].transform(pd.to_numeric, errors='coerce')
    dataset = dataset[dataset['meta.result'] != 'unknown']
    dataset = dataset.groupby('meta.family').filter(lambda x: len(x) >= 10)
    dataset = dataset[dataset[numeric_cols].notna().all(axis='columns')]
    assert dataset['hash'].nunique() == len(dataset)
    dataset.to_csv(DATA_DIR / 'dataset.csv', index=False)
