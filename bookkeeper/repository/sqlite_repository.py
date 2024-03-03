from pony import orm
from typing import Any

from bookkeeper.models.database import db
from bookkeeper.models.category import Category
from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SqliteRepository(AbstractRepository[T]):
    def __init__(self, filename=':memory:') -> None:
        try:
            db.bind(provider='sqlite', filename=filename)
            db.generate_mapping(create_tables=True)
        except orm.BindingError as e:
            if e.args[0] == 'Database object was already bound to SQLite provider':
                pass
            else: raise e

    @orm.db_session
    def add(self, obj: T) -> int:
        instance = obj
        return instance.pk

    @orm.db_session
    def get(self, pk: int)-> T:
        return T[pk]
    
    @orm.db_session
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        if where is None:
            return orm.select(obj for obj in T)[:]
        orm.select(obj for obj in T
                   if all(getattr(obj, attr) == value for attr, value in where.items()))[:]
        
    @orm.db_session
    def update(self, obj: T) -> None:
        orm.commit()
    
    @orm.db_session
    def delete(self, pk: int) -> None:
        T[pk].delete()
