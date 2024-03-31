from datetime import datetime
from typing import Callable, Any
from pony import orm

from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.budget import Budget

class BudgetRepository(SqliteRepository[Budget]):
    def __init__(self, filename: str = ':memory:') -> None:
        super().__init__(filename)
        with orm.db_session():
            try:
                b = Budget.get(pk=1)
            except orm.ObjectNotFound:
                # Initialize daily, weekly, monthly
                b0 = Budget(start = datetime.now(), expiration = datetime.now(), amount=100)
                b1 = Budget(start = datetime.now(), expiration = datetime.now(), amount=1000)
                b2 = Budget(start = datetime.now(), expiration = datetime.now(), amount=10000)

    def add(self, obj: Budget) -> int:
        with orm.db_session:
            instance = obj
            orm.commit()
            return instance.pk

    def get(self, pk: int)-> Any:
        with orm.db_session:
            return Budget[pk]
    
    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> Any:
        with orm.db_session:
            return orm.select(obj for obj in Budget if where(obj))[:]
        
    def update(self, obj: Budget) -> None:
        with orm.db_session:
            orm.commit()

    def delete(self, pk: int) -> None:
        with orm.db_session:
            Budget[pk].delete()