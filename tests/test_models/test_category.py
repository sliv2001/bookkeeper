"""
Тесты для категорий расходов
"""
from inspect import isgenerator

import pytest

from bookkeeper.models.category import Category
from bookkeeper.repository.category_repository import CategoryRepository
from bookkeeper.models.database import db
from pony import orm
from bookkeeper.repository.memory_repository import MemoryRepository

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
    return CategoryRepository()


def test_create_object():

    with orm.db_session:
        c = Category(name='name')

    with orm.db_session:
        c = Category[1]
        assert c.name == 'name'
        assert c.parent is None


def test_reassign():
    """
    class should not be frozen
    """
    with orm.db_session:
        c = Category(name='name')
        c.name = 'test'

    with orm.db_session:
        assert c.name == 'test'

def test_pk_change():
    """
    pk cannot be changed manually
    """
    with orm.db_session:
        c = Category(name='name_pk_change')
        try:
            c.pk = 5
        except: pass

    with orm.db_session:
        pk = c.pk
        try:
            c.pk = 7
        except: pass

    with orm.db_session:
        assert c.name == 'name_pk_change'
        assert c.pk == pk

def test_eq():
    """
    class should implement __eq__ method
    """
    with orm.db_session:
        c1 = Category(name='name_eq1', parent=1)
        c2 = Category(name='name_eq2', parent=1)

    with orm.db_session:
        c3 = Category[4]
        c4 = Category[4]

    with orm.db_session:
        assert c1 != c2
        assert c3 == c4

def test_get_parent_func(repo):
    with orm.db_session:
        c1 = Category(name='parent_get_parent_func')
        pk = repo.add(c1)
        orm.commit()
        c2 = Category(name='name_get_parent_func', parent=pk)
        repo.add(c2)
        orm.commit()
        assert c2.get_parent(repo) == c1

def test_get_parent(repo):
    with orm.db_session:
        c1 = Category(name='name_get_parent_1')

    with orm.db_session:
        c2 = Category(name='name_get_parent_2', parent=c1.pk)

    with orm.db_session:
        assert c2.parent == c1.pk

@orm.db_session
def test_get_all_parents(repo):
    parent_pk = None
    for i in range(5):
        c = Category(name=str(i), parent=parent_pk)
        parent_pk = repo.add(c)
    gen = c.get_all_parents(repo)
    assert isgenerator(gen)
    assert [c.name for c in gen] == ['3', '2', '1', '0']

def test_get_subcategories(repo: CategoryRepository):
    parent_pk = None
    with orm.db_session:

        for i in range(5, 10):
            c = Category(name=str(i), parent=parent_pk)
            parent_pk = repo.add(c)
            orm.commit()

        c = repo.get_all(lambda x: x.name == '0')[0]
        gen = c.get_subcategories(repo)

    with orm.db_session:
        assert isgenerator(gen)
        # using set because order doesn't matter
        assert {c.name for c in gen} == {'1', '2', '3', '4'}

@orm.db_session
def test_create_from_tree(repo):
    tree = [('parent_create_from_tree', None), ('parent_create_from_tree_2', 'parent_create_from_tree')]
    cats = Category.create_from_tree(tree, repo)
    assert len(cats) == len(tree)
    parent = next(c for c in cats if c.name == 'parent_create_from_tree')
    assert parent.parent is None
    c1 = next(c for c in cats if c.name == 'parent_create_from_tree')
    assert c1.parent == None
    c2 = next(c for c in cats if c.name == 'parent_create_from_tree_2')
    assert c2.parent == c1.pk

@orm.db_session
def test_create_from_tree_error(repo):
    tree = [('1', 'parent_create_from_tree_error'), ('parent_create_from_tree_error', None)]
    with pytest.raises(KeyError):
        Category.create_from_tree(tree, repo)
