import pytest

from data_checks import CHECKS, run_checks


def test_clean_data_passes_all_checks(clean_db):
    failed = {name: rows for name, rows in run_checks(clean_db).items() if rows}
    assert failed == {}


# Every planted defect in db/defects.sql must be found by exactly the right check
@pytest.mark.parametrize("check, expected_ids", [
    ("duplicate_customer_emails", ["anna.schmidt@example.com"]),
    ("missing_customer_emails",   [7]),
    ("invalid_customer_emails",   [8]),
    ("non_positive_prices",       [7]),
    ("orders_without_customer",   [107]),
    ("items_without_product",     [110]),
    ("orders_in_the_future",      [108]),
    ("unknown_order_status",      [109]),
    ("non_positive_quantities",   [110]),
    ("order_total_mismatch",      [110]),
])
def test_defects_are_detected(dirty_db, check, expected_ids):
    rows = run_checks(dirty_db)[check]
    assert [row[0] for row in rows] == expected_ids


def test_every_check_is_covered_by_a_defect(dirty_db):
    results = run_checks(dirty_db)
    assert all(results[name] for name in CHECKS), "a check without a matching defect is not tested"
