Polygon - Input Generation for SQL
========

A symbolic reasoning framework for SQL that can **efficiently generate an input database** for multiple queries
such that the query outputs on the generated input satisfy a given property.

----------------

## Prerequisite

#### Docker Installation

- Docker (version 27.5.1 or later)

#### Manual Installation

- Python 3.11 or later
- Z3
- MySQL/MariaDB Server

----------------

## Installation


### Using Docker

In the root directory of the repository, run:

```shell
chmod +x docker.sh && ./docker.sh
```

If you encounter a permission problem, please use sudo to execute ./docker.sh.

The script will build the Docker container and start an interactive shell session.

### Manual Installation

1. Install the dependencies by running

```shell
pip install -r requirements.txt
```

2. Specify the credentials of your MySQL/MariDB server instance by modifying
`DB_CONFIG` in [polygon/testers/mysql_tester.py](polygon/testers/mysql_tester.py).

## Getting Started

Run

```shell
python3 example.py
```

which will run Polygon on an equivalence checking example for two queries.  The expected output is similar to:

```
NEQ Time: 0.262586
[21:36:58] [INFO] Counterexample: {'customers': [['customer_id', 'customer_name', 'email'], [26, None, '37'], [25, None, '37']], 'contacts': [['user_id', 'contact_email', 'contact_name'], [25, '37', '47'], [26, '27', '35']], 'invoices': [['invoice_id', 'user_id', 'price'], [46, 25, 1]]}
[21:36:58] [INFO] Q1: [(46, None, 1, 1, Decimal('1'))]
[21:36:58] [INFO] Q2: [(46, None, 1, 2, 2)]
Refuted: True
```

### Troubleshooting
If you encounter issues like
```
Traceback (most recent call last):
  File "/polygon/example.py", line 5, in <module>
    from polygon.smt import *
ModuleNotFoundError: No module named 'polygon'
```

run `export PYTHONPATH=$(pwd)` in the project's root directory first, and then run the script.

----------------


## How to Reuse or Extend Polygon in Other Projects?

Please refer to [REUSABILITY-GUIDE.md](REUSABILITY-GUIDE.md) for how to integrate or adapt Polygon to benefit your projects.

----------------

## Citation
If you find Polygon helpful in your research, please cite our paper as follows

```
@article{DBLP:journals/pacmpl/ZhaoWW25,
  author       = {Pinhan Zhao and
                  Yuepeng Wang and
                  Xinyu Wang},
  title        = {Polygon: Symbolic Reasoning for {SQL} using Conflict-Driven Under-Approximation
                  Search},
  journal      = {Proc. {ACM} Program. Lang.},
  volume       = {9},
  number       = {{PLDI}},
  pages        = {1315--1340},
  year         = {2025},
  url          = {https://doi.org/10.1145/3729303},
  doi          = {10.1145/3729303}
}
```
