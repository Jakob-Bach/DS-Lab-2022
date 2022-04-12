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

Next, activate the environment.
Install the dependencies with

```bash
python -m pip install -r requirements.txt
```

If you make changes to the environment and you want to persist them, run

```bash
python -m pip freeze > requirements.txt
```

## Task 1: Data Mining Cup 2022 (`Task_1_DMC_2021/`)

## Task 2
