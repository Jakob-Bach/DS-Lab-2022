"""Split for course-internal scoring

Create a time-based train-test split from the orders. As in the real evaluation, the test split
comprises exactly four weeks following the training period. We make sure that all user-item
combinations occuring in the test split also appear in the training split.
"""


import pathlib

import pandas as pd


DATA_DIR = pathlib.Path('data/')
LAST_TRAIN_DAY = pd.Timestamp('2020-12-31')


if __name__ == '__main__':
    orders = pd.read_csv(DATA_DIR / 'orders.csv', sep='|', parse_dates=['date'])

    orders_train = orders[orders['date'] <= LAST_TRAIN_DAY]
    solution = orders_train[['userID', 'itemID']].copy()

    # Option 1: Keep all train user-item combinations in test (as an alternative: sample)
    # --- no additional code necessary ---

    # # Option 2: Keep only train user-item combinations in test that appear in DMC test set:
    # solution = solution.merge(pd.read_csv(DATA_DIR / 'submission.csv', sep='|')[['userID', 'itemID']])

    # # Option 3: Keep only user-item combinations in test that appear at least twice in train:
    # solution = solution.groupby(['userID', 'itemID']).filter(lambda x: len(x) >= 2)

    # Remove repeated orders:
    solution.drop_duplicates(inplace=True)
    # Find the first date after training period when item is purchased by a user
    first_replenishment = orders[orders['date'] > LAST_TRAIN_DAY].groupby(
        ['userID', 'itemID'])['date'].min().reset_index()
    # Add this information; note that some items might not be replenished, and replenishment of
    # items not appearing in "solution" is not interesting for us -> therefore LEFT join:
    solution = solution.merge(first_replenishment, how='left')
    # Create target variable by discretizing replenishment date into four weeks + out of test period
    intervals = [LAST_TRAIN_DAY + pd.Timedelta(days=x * 7) for x in range(5)]  # left-open intervals
    solution['prediction'] = pd.cut(solution['date'], bins=intervals, labels=[1, 2, 3, 4])
    solution['prediction'] = solution['prediction'].astype('Int64').fillna(0)
    solution.drop(columns='date', inplace=True)
    # Order by userID and itemID to remove any temporal information:
    solution.sort_values(by=['userID', 'itemID'], inplace=True)
    # Create submission by setting target column emtpy:
    submission = solution[['userID', 'itemID']].copy()
    submission['prediction'] = float('nan')

    orders_train.to_csv(DATA_DIR / 'split_orders.csv', sep='|', index=False)
    submission.to_csv(DATA_DIR / 'split_submission.csv', sep='|', index=False)
    solution.to_csv(DATA_DIR / 'split_solution.csv', sep='|', index=False)
