from datetime import datetime, timedelta
from pony import orm

import pytest

from bookkeeper.repository.budget_repository import BudgetRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.database import db

@pytest.fixture(autouse=True)
def run_around_tests():
    try:
        db.bind(provider='sqlite', filename=":memory:")
        db.generate_mapping(create_tables=True)
    except orm.BindingError as e:
        if e.args[0] == 'Database object was already bound to SQLite provider':
            pass
        else: raise e

@orm.db_session
def test_budget_add():
    b1 = Budget(start=datetime.now(), expiration=datetime.now(), amount=10000)
    b2 = Budget(start=datetime.now(), expiration=datetime.now()+timedelta(days=+1), amount=10000)
    orm.commit()
    assert b1.amount == b2.amount

@orm.db_session
def test_budget_add_short():
    b = Budget(expiration=datetime.now()+timedelta(days=+1), amount = 100)
    orm.commit()
    assert b.amount == 100
