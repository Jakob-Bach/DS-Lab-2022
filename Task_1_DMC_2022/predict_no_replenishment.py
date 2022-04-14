"""Predict no replenishment

Script that creates a simple baseline solution for the course-internal splitting: For each
user-item combination, predict that there will be no replenishment in the test period. This makes
sense, as even in the full DMC training period of eight months, most user-item combinations only
appear once.
"""


import pathlib

import pandas as pd


DATA_DIR = pathlib.Path('data/')


if __name__ == '__main__':
    submission = pd.read_csv(DATA_DIR / 'split_submission.csv', sep='|')
    submission['prediction'] = 0
    submission.to_csv(DATA_DIR / 'no-replenishment_solution.csv', sep='|', index=False)
