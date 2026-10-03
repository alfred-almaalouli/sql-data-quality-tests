import queries


def run(db, sql):
    return db.execute(sql).fetchall()


def test_revenue_per_category(clean_db):
    assert run(clean_db, queries.REVENUE_PER_CATEGORY) == [
        ("Electronics", 2037.70),
        ("Furniture", 149.00),
        ("Books", 88.80),
    ]


def test_cancelled_orders_are_not_counted_as_revenue(clean_db):
    categories = dict(run(clean_db, queries.REVENUE_PER_CATEGORY))
    # the only furniture lamp was in a cancelled order
    assert categories["Furniture"] == 149.00


def test_top_customers(clean_db):
    assert run(clean_db, queries.TOP_CUSTOMERS) == [
        ("Omar Haddad", 2, 1087.90),
        ("Anna Schmidt", 2, 1027.80),
        ("Lena Fischer", 1, 159.80),
    ]


def test_customers_without_orders(clean_db):
    assert run(clean_db, queries.CUSTOMERS_WITHOUT_ORDERS) == [("Sara Klein",)]


def test_products_never_sold(clean_db):
    assert run(clean_db, queries.PRODUCTS_NEVER_SOLD) == []


def test_monthly_revenue_with_running_total(clean_db):
    assert run(clean_db, queries.MONTHLY_REVENUE_WITH_RUNNING_TOTAL) == [
        ("2025-06", 1176.80, 1176.80),
        ("2025-07", 1098.70, 2275.50),
    ]


def test_cancellation_rate_per_city(clean_db):
    assert run(clean_db, queries.CANCELLATION_RATE_PER_CITY) == [
        ("Dortmund", 2, 0.0),
        ("Düsseldorf", 1, 0.0),
        ("Essen", 3, 33.3),
    ]
