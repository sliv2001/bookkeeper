"""
This is the parent class of all the repository classes used in project.
"""

from pony import orm
from typing import Any

from bookkeeper.models.database import db
from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SqliteRepository(AbstractRepository[T]):
    def __init__(self, filename: str =':memory:') -> None:
        try:
            db.bind(provider='sqlite', filename=filename, create_db=True)
            db.generate_mapping(create_tables=True)
        except orm.BindingError as e:
            if e.args[0] == 'Database object was already bound to SQLite provider':
                pass
            else: raise
