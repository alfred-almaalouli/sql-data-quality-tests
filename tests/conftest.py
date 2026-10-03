import pytest

from data_checks import create_database


@pytest.fixture
def clean_db():
    conn = create_database("schema.sql", "seed.sql")
    yield conn
    conn.close()


@pytest.fixture
def dirty_db():
    conn = create_database("schema.sql", "seed.sql", "defects.sql")
    yield conn
    conn.close()
