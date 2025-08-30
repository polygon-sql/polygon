## Reusability Guide

In this document, we provide a detailed guide on how to run Polygon on new inputs, and how to extend Polygon
to support new features for further research.


- ### How to run Polygon on a new inputs?

Polygon's highly modularized structure makes it easy to integrate into other projects and adapt for new inputs.

In `example.py`, we provide an equivalence checking example that showcases the interface of Polygon.

In what follows, we walk the reader through an example to explain the Polygon's interface and demonstrate how it
can be used with new inputs.

1. **Specify the schema and integrity constraints**

Firstly, change the schema in `example.py` to the new schema.
Consider the following schema:

```
schema = [
    {
        "TableName": "Employees",
        "PKeys": [
            {
                "Name": "emp_id",
                "Type": "int"
            }
        ],
        "FKeys": [],
        "Others": [
            {
                "Name": "name",
                "Type": "varchar"
            },
            {
                "Name": "age",
                "Type": "int"
            }
        ]
    }
]
```

which corresponds to a table `Employees` with primary key `emp_id` and two
attributes `name` and `age`.

Then, specify `constraints` in `example.py` as follows:

```
constraints = [{'distinct': ['Employees.emp_id']}]
```

which means that the `emp_id` attribute in the `Employees` table should be distinct
(as it is a primary key).


2. **Specify the SQL queries**

Next, specify the SQL queries in `example.py`.  For example,


```python
queries = [
    """
    SELECT emp_id FROM Employees WHERE age > 30
    """,

    """
    SELECT emp_id FROM Employees WHERE age >= 30
    """
]
```

The first query selects the `emp_id` from the `Employees` table where the `age` is greater than 30,
whereas the second query selects the `emp_id` from the `Employees` table where the `age` is greater than or equal to 30.

As we can see, the two queries are semantically not equivalent, and are expected to be refuted by Polygon.

(3) **Run Polygon on the new input**

Running Polygon on the new input as specified above by running `python3 example.py`, the user may expect an output similar to:

```
NEQ Time: 0.083584
[22:47:14] [INFO] Counterexample: {'employees': [['emp_id', 'name', 'age'], [7, '5', 31], [8, '6', 30]]}
[22:47:14] [INFO] Q1: [(7,)]
[22:47:14] [INFO] Q2: [(7,), (8,)]
Refuted: True
```

which means that the SQL queries are successfully refuted, with an input database (counterexample) shown above.
The output also shows the results of executing the SQL queries on the generated input.

The use of Polygon for the disambiguation application generally follows the same steps as above,
except that instead of `env.check`, `env.disambiguate` needs to be called and it takes
a list of queries as input. The output will be the same as in the equivalence
refutation application where if the set of provided queries can be disambiguated,
the output will be an input database.

- ### How to extend Polygon to support new application conditions?

As a general-purpose symbolic reasoning engine for SQL, Polygon is designed to be capable of generating inputs
that satisfy arbitrary conditions expressed in SMT.

To do so, the user needs to modify the `polygon/environment.py` file. In particular, the user will create
a new method similar to `check` or `disambiguate` in which SMT formula for the desired application condition
will be specified and conjoined by using `self.formulas.append()`.

For example, consider a scenario that a user wants to generate inputs satisfying the condition that the output
table of a query is non-empty, the user may write a formula that encodes there is at least one tuple in the
output table is *not deleted*, storing it in a variable, for instance, `non_empty_cond`, and then conjoin it
to the existing formulas by `self.formulas.append(non_empty_cond)`.


- ### How to extend Polygon to support new features?

The user may want to extend Polygon to support new features, such as SQL expressions.

Since Polygon has already supported all commonly used clause-level SQL operators, it would be more likely
that the user wants to extend Polygon to support new SQL *expressions*.

To do so, the user needs to modify the `polygon/visitors/expression_encoder.py` file.
The user may want to add a branch in the `visit_Expression` method to handle the new expression.

For example, the following code snippet shows how to handle the `DATE_ADD` expression in SQL:

```python
if node.operator == 'date_add':
    date_val, date_null = node.args[0].accept(self)
    days_to_add, _ = node.args[1].accept(self)
    return date_val + days_to_add, date_null
```

In particular, `date_val` and `date_null` stores the symbolic value and nullability of the first argument
of the `DATE_ADD` expression (the attribute). And `days_to_add` stores the how many days to add to the date.
Finally, the return value will be a tuple consisting of the returning symbolic value and nullability for the
expression.