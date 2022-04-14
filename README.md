# Data Science Laboratory Course 2022

This is the supervisor repo of the ["Data Science Laboratory Course"](https://dbis.ipd.kit.edu/english/3128.php) at KIT in 2022.
Students worked on two subtasks:

- the [Data Mining Cup 2022](https://www.data-mining-cup.com/dmc-2022/)
- a research problem from the field of SAT solving

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

## Task 2
