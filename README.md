# Data Science Laboratory Course 2022

This is the supervisor repo of the ["Data Science Laboratory Course"](https://dbis.ipd.kit.edu/english/3128.php) at KIT in 2022.
Students worked on two subtasks:

- the [Data Mining Cup 2022](https://www.data-mining-cup.com/dmc-2022/)
- a research problem from the field of [SAT solving](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)

The repo provides files for preparing the datasets, some basic exploration, course-internal splitting, scoring, and demo submissions for that.

## Setup

We use Python with version `3.8`.
We recommend to set up a virtual environment to install the dependencies, e.g., with `virtualenv`:

```bash
python -m virtualenv -p <path/to/right/python/executable> <path/to/env/destination>
```

or with `conda`:

```bash
conda create --name ds-lab-2022 python=3.8
```

Next, activate the environment with either

- `conda activate ds-lab-2022` (`conda`)
- `source <path/to/env/destination>/bin/activate` (`virtualenv`, Linux)
- `<path\to\env\destination>\Scripts\activate` (`virtualenv`, Windows)

Install the dependencies with

```bash
python -m pip install -r requirements.txt
```

If you make changes to the environment and you want to persist them, run

```bash
python -m pip freeze > requirements.txt
```

To make this environment available for notebooks, run

```
ipython kernel install --user --name=ds-lab-2022-kernel
```

To actually launch `Jupyter Notebook`, run

```
jupyter notebook
```

## Task 1: Data Mining Cup 2022 (`Task_1_DMC_2022/`)

The first task of the course is identical to the task of the `Data Mining Cup 2022`.
We only add a course-internal splitting and scoring to compare the students' solutions.

### Preparation

Download the DMC task from the [website](https://www.data-mining-cup.com/dmc-2022/).
Place the four CSVs in a folder called `data/` in the folder `Task_1_DMC_2022/`.

### Exploration

The notebook `Exploration.ipynb` contains basic exploration (mainly statistics) of the four CSVs.

### Scoring

- `split.py` creates a temporal train-test split.
  It takes all orders up to a certain day as training data and the following four weeks for testing.
  It creates corresponding files with (training) oders, a submission template, and the solution.
- `predict_no_replenishment.py` creates a baseline solution for the train-test split,
  constantly predicting no replenishment.
- `predict_interpolated_orders.py` creates a more sophisticated prediction
  (which still ignores item features and uses no prediction model):
  For items purchased on at least two days by the particular customer in the training period,
  it computes how long the ordered amount lasted on average, and uses this information to estimate
  the next replenishment date based on the amount ordered last.
  If this date falls after the test period, or a user did not order an item on at least two dates
  (which happens in most cases), predict no replenishment.
- `score.py` scores submissions of students for the course-internal train-test split.
  It also checks the validity of the submissions.
- `check_submission_identity.py` checks whether identically-named submission files have the same
  content (= checks reproducibility).

## Task 2: SAT Solving (`Task_2_SAT_Solving/`)

The second task of the course works with features of SAT instances
from the [Global Benchmark Database (`GBD`)](https://gbd.iti.kit.edu/).
We have two prediction targets, which are assigned to different teams of students:

- Is the instance satisfiable or not (column `result` in database `meta`)?
- To which family does the instance belong (column `family` in database `meta`)?

Besides exploring the data, students should use classification as well as clustering approaches.

### Preparation

`prepare_data.py` pre-processes the dataset:

- download databases with meta data and instance features from `GBD`
- merge databases
- filter instances:
  - known satisfiablity result
  - at least 10 members in family (which is still quite few)
  - no NAs in instance features

### Scoring

- `split.py` creates a stratified holdout split for both targets.
- `cluster_kmeans.py` creates a clustering-based solution for predictions (which, unsurprisingly, is bad).
- `predict_majority.py` creates a baseline solution that constantly predicts the majoriy class.
- `predict_tree.py` creates a simple solution with the help of a decision tree.
- `score.py` scores submissions of students for the course-internal holdout split.
  Works for both targets and classification as well as clustering.
