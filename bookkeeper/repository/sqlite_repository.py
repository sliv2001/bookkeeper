"""
This module contains the parent class of all the repository classes used in project.
"""

from pony import orm

from bookkeeper.models.database import db
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SqliteRepository(AbstractRepository[T]):
    """
    This is the parent class of all the repository classes used in project.
    """
    def __init__(self, filename: str = ':memory:') -> None:
        try:
            db.bind(provider='sqlite', filename=filename, create_db=True)
            db.generate_mapping(create_tables=True)
        except orm.BindingError as exc:
            if exc.args[0] == 'Database object was already bound to SQLite provider':
                pass
            else:
                raise
