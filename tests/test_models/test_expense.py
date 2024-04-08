from datetime import datetime
from pony import orm

import pytest

from bookkeeper.repository.expense_repository import ExpenseRepository
from bookkeeper.models.expense import Expense
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

@pytest.fixture
def repo():
    return ExpenseRepository()

@orm.db_session
def test_create_with_full_args_list():
    e = Expense(amount=100, category=1, expense_date=datetime.now(),
                added_date=datetime.now(), comment='test')
    orm.commit()
    assert e.amount == 100
    assert e.category.prim_key == 1

@orm.db_session
def test_create_brief():
    e = Expense(amount=100, category=1)
    orm.commit()
    assert e.amount == 100
    assert e.category.prim_key == 1

@orm.db_session
def test_can_add_to_repo(repo):
    e = Expense(amount=100, category=1)
    prim_key = repo.add(e)
    assert e.prim_key == prim_key
