"""Predict interpolated orders

Script that creates a simple (well, at least in terms of describing it, while the code is not
trivial) non-constant solution for the course-internal splitting:
Check if the customer under discussion has ordered the item under discussion at least twice in the
training period. If yes, compute the average consumption per day from the first purchase till the
last purchase. Use this information to interpolate how long the last purchase will last. In case a
user-item combination does not appear twice (majority of cases), predict no replenishment. Same goes
for the case that the expected replenishment will only be after the test period. In case it will be
before the test period, predict replenishment in the first week.
"""


import pathlib

import pandas as pd

DATA_DIR = pathlib.Path('data/')
LAST_TRAIN_DAY = pd.Timestamp('2020-12-31')


if __name__ == '__main__':
    orders = pd.read_csv(DATA_DIR / 'split_orders.csv', sep='|', parse_dates=['date'])
    submission = pd.read_csv(DATA_DIR / 'split_submission.csv', sep='|')

    # Get the user-item combinations that occur on more than just one date:
    order_counts = orders.groupby(['userID', 'itemID'])['date'].nunique().reset_index()
    order_counts = order_counts[order_counts['date'] > 1]
    repeated_orders = orders.merge(order_counts[['userID', 'itemID']].drop_duplicates())
    # Separate between the last order date for each user-item combination and all orders before
    # (note that there might be multiple orders on a date):
    last_order_dates = repeated_orders.groupby(['userID', 'itemID'])['date'].max().reset_index()
    not_last_orders = repeated_orders.merge(last_order_dates, how='left', indicator=True)
    not_last_orders = not_last_orders[not_last_orders['_merge'] == 'left_only']
    last_orders = repeated_orders.merge(last_order_dates)
    assert len(last_orders) + len(not_last_orders) == len(repeated_orders)
    # Compute average consumption (order amount) between first and last date:
    consumed_amount = not_last_orders.groupby(['userID', 'itemID'])['order'].sum().reset_index()
    consumed_amount.rename(columns={'order': 'consumed'}, inplace=True)
    first_order_dates = repeated_orders.groupby(['userID', 'itemID'])['date'].min().reset_index()
    first_order_dates.rename(columns={'date': 'first_date'}, inplace=True)
    last_order_dates.rename(columns={'date': 'last_date'}, inplace=True)
    consumed_amount = consumed_amount.merge(first_order_dates)
    consumed_amount = consumed_amount.merge(last_order_dates)
    consumed_amount['avg_consumption'] = consumed_amount['consumed'] /\
        (consumed_amount['last_date'] - consumed_amount['first_date']).apply(lambda x: x.days)
    # Interpolate consumption to future:
    last_orders = last_orders.groupby(['userID', 'itemID'])['order'].sum().reset_index()
    prediction = consumed_amount.merge(last_orders)
    prediction['expected_duration'] = (prediction['order'] / prediction['avg_consumption']).round()
    prediction['expected_date'] = prediction['last_date'] + pd.to_timedelta(
        prediction['expected_duration'], unit='days')
    # Discretize to match prediction format:
    intervals = [LAST_TRAIN_DAY + pd.Timedelta(days=x * 7) for x in range(5)]  # left-open intervals
    intervals[0] = pd.Timestamp('2020-01-01')  # week 1 also catches expected reorders before it
    prediction['prediction'] = pd.cut(prediction['expected_date'], bins=intervals,
                                      labels=[1, 2, 3, 4])
    prediction = prediction[submission.columns]
    # Fill in baseline for remaining user-item combinations (not ordered twice or expected
    # replenishment after test period):
    submission.drop(columns='prediction', inplace=True)
    submission = submission.merge(prediction, how='left')
    submission['prediction'] = submission['prediction'].astype('Int64').fillna(0)

    submission.to_csv(DATA_DIR / 'interpolated-orders_solution.csv', sep='|', index=False)
