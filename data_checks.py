"""Data quality checks for the shop database.

Every check is a SQL query that returns the rows that break a rule.
An empty result means the check passed.
"""
import sqlite3
import sys
from pathlib import Path

DB_DIR = Path(__file__).parent / "db"

VALID_STATUSES = ("NEW", "PAID", "SHIPPED", "DELIVERED", "CANCELLED")

CHECKS = {
    "duplicate_customer_emails": """
        SELECT email, COUNT(*) AS times
        FROM customers
        WHERE email IS NOT NULL
        GROUP BY LOWER(email)
        HAVING COUNT(*) > 1
    """,
    "missing_customer_emails": """
        SELECT customer_id, name FROM customers
        WHERE email IS NULL OR TRIM(email) = ''
    """,
    "invalid_customer_emails": """
        SELECT customer_id, email FROM customers
        WHERE email IS NOT NULL AND email NOT LIKE '%_@_%._%'
    """,
    "non_positive_prices": """
        SELECT product_id, name, price FROM products WHERE price <= 0
    """,
    "orders_without_customer": """
        SELECT o.order_id, o.customer_id
        FROM orders o
        LEFT JOIN customers c ON c.customer_id = o.customer_id
        WHERE c.customer_id IS NULL
    """,
    "items_without_product": """
        SELECT i.order_id, i.product_id
        FROM order_items i
        LEFT JOIN products p ON p.product_id = i.product_id
        WHERE p.product_id IS NULL
    """,
    "orders_in_the_future": """
        SELECT order_id, order_date FROM orders WHERE order_date > DATE('now')
    """,
    "unknown_order_status": f"""
        SELECT order_id, status FROM orders
        WHERE status NOT IN ({", ".join(f"'{s}'" for s in VALID_STATUSES)})
    """,
    "non_positive_quantities": """
        SELECT order_id, product_id, quantity FROM order_items WHERE quantity <= 0
    """,
    "order_total_mismatch": """
        SELECT o.order_id, o.total, ROUND(SUM(i.quantity * i.unit_price), 2) AS items_total
        FROM orders o
        JOIN order_items i ON i.order_id = o.order_id
        GROUP BY o.order_id
        HAVING ABS(o.total - SUM(i.quantity * i.unit_price)) > 0.01
    """,
}


def create_database(*sql_files, path=":memory:"):
    conn = sqlite3.connect(path)
    for name in sql_files:
        conn.executescript((DB_DIR / name).read_text(encoding="utf-8"))
    return conn


def run_checks(conn):
    """Returns {check name: list of rows that break the rule}."""
    return {name: conn.execute(sql).fetchall() for name, sql in CHECKS.items()}


def print_report(results):
    failed = 0
    for name, rows in results.items():
        if rows:
            failed += 1
            print(f"FAIL  {name} ({len(rows)} row(s))")
            for row in rows:
                print(f"      {row}")
        else:
            print(f"PASS  {name}")
    print(f"\n{len(results) - failed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    files = ["schema.sql", "seed.sql"] + (["defects.sql"] if "--with-defects" in sys.argv else [])
    sys.exit(1 if print_report(run_checks(create_database(*files))) else 0)
