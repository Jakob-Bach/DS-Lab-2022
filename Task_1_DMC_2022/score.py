"""Course-internal scoring

Script that finds all submission files named like `<<Teamname>>_solution.csv` in some directory,
checks their validity, and scores them against a ground truth (according the the DMC's rules).
"""


import csv
import pathlib

import pandas as pd


DATA_DIR = pathlib.Path('data/')  # needs to contain submissions and ground truth solution


def validate_submission(submission: pd.DataFrame, ground_truth: pd.DataFrame) -> str:
    if submission.shape[0] != ground_truth.shape[0]:
        return 'Number of predictions wrong (could also be issue with header).'
    if submission.shape[1] != ground_truth.shape[1]:
        return 'Number of columns wrong (index column might be saved).'
    if list(submission) != list(ground_truth):
        return 'At least one column name wrong (might be quoted).'
    if (submission.dtypes != 'int64').any():
        return 'At least one column does not contain integers.'
    if submission.isna().any().any():
        return 'At least one NA.'
    if (submission['userID'] != ground_truth['userID']).any():
        return 'New or unordered userID.'  # if order irrelevant, could check length of outer join
    if (submission['itemID'] != ground_truth['itemID']).any():
        return 'New or unordered itemID.'
    if not submission['prediction'].isin([0, 1, 2, 3, 4]).all():
        return 'At least one invalid prediction.'
    return 'Valid.'


# Score according to DMC:
# - one point if replenishment no/yes predicted correctly
# - three points if week predicted correctly
def score_submission(submission: pd.DataFrame, ground_truth: pd.DataFrame) -> float:
    submission = submission.merge(ground_truth, on=['userID', 'itemID'])
    score = ((submission['prediction_x'] == 0) == (submission['prediction_y'] == 0)).sum()
    score = score + 2 * ((submission['prediction_x'] != 0) &
                         (submission['prediction_x'] == submission['prediction_y'])).sum()
    return score


if __name__ == '__main__':
    if not DATA_DIR.exists():
        FileNotFoundError(f'"{DATA_DIR}" does not exist.')
    ground_truth_file = DATA_DIR / 'split_solution.csv'
    ground_truth = pd.read_csv(ground_truth_file, sep='|')
    submission_files = list(DATA_DIR.glob('*_solution.csv'))
    submission_files.remove(ground_truth_file)
    results = []
    for submission_file in submission_files:
        submission = pd.read_csv(submission_file, sep='|', quoting=csv.QUOTE_NONE, header=0,
                                 escapechar=None, encoding='utf-8')
        team_name = submission_file.stem.replace('_solution', '')
        validity_status = validate_submission(submission=submission, ground_truth=ground_truth)
        if validity_status == 'Valid.':
            score = score_submission(submission=submission, ground_truth=ground_truth)
        else:
            score = float('nan')
        results.append({'Team': team_name, 'Score': score, 'Validity': validity_status})
    results = pd.DataFrame(results).sort_values(by='Score', ascending=False)
    print(results)
