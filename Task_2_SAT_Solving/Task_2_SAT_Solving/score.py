"""Course-internal scoring on SAT-solving data

Script that finds all submission files in some directory, checks their validity, and scores them
against a ground truth, either for classification or for regression.
"""


import csv
import pathlib

import pandas as pd
import sklearn.metrics

import split


DATA_DIR = pathlib.Path('data/')  # needs to contain submissions and ground truth solution
CLUSTERING = False


def validate_submission(submission: pd.DataFrame, ground_truth: pd.DataFrame, target: str) -> str:
    if submission.shape[0] != ground_truth.shape[0]:
        return 'Number of predictions wrong (could also be issue with header).'
    if submission.shape[1] != ground_truth.shape[1]:
        return 'Number of columns wrong (index column might be saved).'
    if list(submission) != list(ground_truth):
        return 'At least one column name wrong (might be quoted).'
    if submission.isna().any().any():
        return 'At least one NA.'
    if CLUSTERING:
        if submission[target].dtype != 'int64':
            return 'Predicted cluster indices are not integer.'
    else:
        if submission[target].dtype == 'int64':
            return 'Predicted class labels are integer.'
    return 'Valid.'


def score_submission(submission: pd.DataFrame, ground_truth: pd.DataFrame, target: str) -> float:
    submission = submission.merge(ground_truth, on='hash')
    if CLUSTERING:
        return sklearn.metrics.normalized_mutual_info_score(
            labels_true=submission[f'{target}_y'], labels_pred=submission[f'{target}_x'])
    return sklearn.metrics.accuracy_score(
        y_true=submission[f'{target}_y'], y_pred=submission[f'{target}_x'])


if __name__ == '__main__':
    for target in split.TARGETS:
        print('Target:', target)
        results = []
        ground_truth = pd.read_csv(DATA_DIR / f'{target}_y_test.csv')
        submission_files = list(DATA_DIR.glob(f'{target}_*_prediction.csv'))
        for submission_file in submission_files:
            submission = pd.read_csv(submission_file, sep=',', quoting=csv.QUOTE_NONE, header=0,
                                     escapechar=None, encoding='utf-8')
            team_name = submission_file.stem.replace(f'{target}_', '').replace('_prediction', '')
            validity_status = validate_submission(submission=submission, ground_truth=ground_truth,
                                                  target=target)
            if validity_status == 'Valid.':
                score = score_submission(submission=submission, ground_truth=ground_truth,
                                         target=target)
            else:
                score = float('nan')
            results.append({'Team': team_name, 'Score': score, 'Validity': validity_status})
        results = pd.DataFrame(results).sort_values(by='Score', ascending=False)
        print(results.round(2), end='\n\n')
