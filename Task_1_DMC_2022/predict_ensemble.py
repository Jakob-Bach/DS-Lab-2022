"""Prediction ensemble

Script that retrieves all submission files from a directory and creates multiple ensemble solutions
from them by using statistical aggregates and tree-based stacking for all possible combinations of
valid submissions. Stacking might overfit, as it uses the ground-truth labels for training.
"""


import csv
import functools
import itertools
import pathlib

import pandas as pd
import sklearn.tree
import tqdm

import score


INPUT_DIR = pathlib.Path('data/')  # needs to contain submissions and ground truth solution
OUTPUT_DIR = pathlib.Path('data/')


if __name__ == '__main__':
    if not INPUT_DIR.exists():
        FileNotFoundError(f'"{INPUT_DIR}" does not exist.')
    if not OUTPUT_DIR.exists():
        print(f'Output directory "{OUTPUT_DIR}" does not exist. We create it.')
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ground_truth_file = INPUT_DIR / 'split_solution.csv'  # used for training stacking model
    ground_truth = pd.read_csv(ground_truth_file, sep='|')
    submission_files = list(INPUT_DIR.glob('*_solution.csv'))
    submission_files.remove(ground_truth_file)
    submissions = []
    for submission_file in submission_files:
        submission = pd.read_csv(submission_file, sep='|', quoting=csv.QUOTE_NONE, header=0,
                                 escapechar=None, encoding='utf-8')
        team_name = submission_file.stem.replace('_solution', '')
        if score.validate_submission(submission=submission, ground_truth=ground_truth) == 'Valid.':
            submissions.append(submission.rename(columns={'prediction': team_name}))
    progress_bar = tqdm.tqdm(desc='Combining solutions', total=(2 ** len(submissions) - 1))
    for ensemble_size in range(1, len(submissions) + 1):
        for ensemble_submissions in itertools.combinations(submissions, ensemble_size):
            ensemble_data = functools.reduce(pd.merge, ensemble_submissions)  # join all submissions
            prediction_cols = [x for x in ensemble_data.columns if x not in ('userID', 'itemID')]
            model = sklearn.tree.DecisionTreeClassifier(random_state=25)
            model.fit(X=ensemble_data[prediction_cols],
                      y=ensemble_data.merge(ground_truth)['prediction'])
            submission['prediction'] = model.predict(X=ensemble_data[prediction_cols])
            submission.to_csv(OUTPUT_DIR / ('_'.join(prediction_cols) + '_stacking_solution.csv'),
                              sep='|', index=False)
            for func in ['min', 'mean', 'max', 'mode']:  # instance methods of DataFrame
                prediction = getattr(ensemble_data[prediction_cols], func)(axis='columns')
                if func == 'mode':
                    prediction = prediction[0]  # there might be multiple modes
                submission['prediction'] = prediction.round().astype(int)
                submission.to_csv(OUTPUT_DIR / f'{"_".join(prediction_cols)}_{func}_solution.csv',
                                  sep='|', index=False)
            progress_bar.update()
    progress_bar.close()
