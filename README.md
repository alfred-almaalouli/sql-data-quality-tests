# SQL Data Quality Tests

![Data Tests](https://github.com/alfred-almaalouli/sql-data-quality-tests/actions/workflows/tests.yml/badge.svg)

A small online shop database (customers, products, orders, order items) with **automated data quality checks** and **tested SQL reports**. Written in **SQL** (SQLite) and **Python**, tested with **pytest** and run in **GitHub Actions**.

Bad data is one of the most common sources of bugs. This project shows how I test data: every business rule is written as a SQL query that returns the rows breaking the rule.

## Data quality checks

| Check | Rule |
|-------|------|
| duplicate_customer_emails | an e-mail address belongs to only one customer (case-insensitive) |
| missing_customer_emails | every customer has an e-mail address |
| invalid_customer_emails | e-mail addresses have a valid format |
| non_positive_prices | product prices are greater than 0 |
| orders_without_customer | every order belongs to an existing customer (referential integrity) |
| items_without_product | every order item points to an existing product |
| orders_in_the_future | order dates are not in the future |
| unknown_order_status | status is one of NEW, PAID, SHIPPED, DELIVERED, CANCELLED |
| non_positive_quantities | quantities are at least 1 |
| order_total_mismatch | the order total equals the sum of its items |

## How it is tested

- `db/seed.sql` contains **clean data** – all checks must pass.
- `db/defects.sql` adds rows with **planted defects** (duplicate e-mail, unknown customer, wrong total, ...). The tests check that every defect is found by the right check – and that no check exists without a matching defect.
- `queries.py` answers business questions (revenue per category, top customers, customers without orders, monthly revenue with running total, cancellation rate per city). The tests compare the results with values calculated by hand.

SQL used: `JOIN` / `LEFT JOIN`, `GROUP BY` / `HAVING`, subqueries (`EXISTS`, `NOT IN`), `CASE`, window function (`SUM() OVER`), date functions.

## Run it

```bash
python data_checks.py                  # checks on clean data -> all PASS
python data_checks.py --with-defects   # checks with planted defects -> FAIL with the broken rows
pytest -v                              # all tests
```

Example output with defects:

```
FAIL  order_total_mismatch (1 row(s))
      (110, 100.0, 49.89)
```

## Project structure

```
db/schema.sql        tables
db/seed.sql          clean test data
db/defects.sql       rows with data quality problems
data_checks.py       data quality rules as SQL queries + report
queries.py           business reports in SQL
tests/               pytest tests
```

## Tech stack

SQL (SQLite) · Python · pytest · GitHub Actions

## Author

Alfred Al Maalouli – [GitHub](https://github.com/alfred-almaalouli)
