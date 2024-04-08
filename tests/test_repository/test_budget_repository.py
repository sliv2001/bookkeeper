from datetime import datetime, timedelta
from pony import orm

import pytest

from bookkeeper.repository.budget_repository import BudgetRepository
from bookkeeper.models.budget import Budget

@pytest.fixture
def b_repo():
    return BudgetRepository()

def test_add_get(b_repo):
    with orm.db_session:
        res = Budget(expiration=datetime.now(), amount=1000)
        res_prim_key = b_repo.add(res)

    res1 = b_repo.get(res_prim_key)
    assert res_prim_key != None
    assert res1.prim_key == res.prim_key
    assert res1.amount == res.amount
    assert res1.expiration == res.expiration
    assert res1.start == res.start
    # For some reason, __eq__ does not work here despite that all fields are the same
    # assert res == res1

def test_add_multiple(b_repo):
    with orm.db_session:
        for i in range(1, 20):
            b_repo.add(Budget(expiration=datetime.now(), amount=i))

    list1 = b_repo.get_all()
    list2 = b_repo.get_all(lambda x: x.amount > 0)
    assert len(list1) == len(list2)
    for i in range(len(list1)):
        assert list1[i].amount == list2[i].amount
        assert list1[i].start == list2[i].start
        assert list1[i].expiration == list2[i].expiration

def test_update(b_repo):
    with orm.db_session:
        b = b_repo.get(1)
        b.amount = 500
        b_repo.update(b)
    
    new_amount = b_repo.get(1).amount
    assert new_amount == 500

def test_delete(b_repo):
    b_repo.delete(1)
    with pytest.raises(orm.ObjectNotFound):
        b_repo.get(1)