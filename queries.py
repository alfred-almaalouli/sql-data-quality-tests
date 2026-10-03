"""Business questions answered with SQL (joins, grouping, subqueries, window functions)."""

# Revenue only counts orders that were not cancelled
REVENUE_PER_CATEGORY = """
    SELECT p.category, ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
    FROM order_items i
    JOIN products p ON p.product_id = i.product_id
    JOIN orders o   ON o.order_id = i.order_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY p.category
    ORDER BY revenue DESC
"""

TOP_CUSTOMERS = """
    SELECT c.name, COUNT(o.order_id) AS orders, ROUND(SUM(o.total), 2) AS spent
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY c.customer_id
    ORDER BY spent DESC
    LIMIT 3
"""

CUSTOMERS_WITHOUT_ORDERS = """
    SELECT c.name
    FROM customers c
    WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
    ORDER BY c.name
"""

PRODUCTS_NEVER_SOLD = """
    SELECT p.name
    FROM products p
    WHERE p.product_id NOT IN (SELECT DISTINCT product_id FROM order_items)
    ORDER BY p.name
"""

MONTHLY_REVENUE_WITH_RUNNING_TOTAL = """
    SELECT month,
           revenue,
           ROUND(SUM(revenue) OVER (ORDER BY month), 2) AS running_total
    FROM (
        SELECT STRFTIME('%Y-%m', order_date) AS month, ROUND(SUM(total), 2) AS revenue
        FROM orders
        WHERE status <> 'CANCELLED'
        GROUP BY month
    )
    ORDER BY month
"""

CANCELLATION_RATE_PER_CITY = """
    SELECT c.city,
           COUNT(*) AS orders,
           ROUND(100.0 * SUM(CASE WHEN o.status = 'CANCELLED' THEN 1 ELSE 0 END) / COUNT(*), 1) AS cancel_rate
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY c.city
    ORDER BY c.city
"""
