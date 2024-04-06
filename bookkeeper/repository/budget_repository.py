from datetime import datetime
from typing import Callable, Any
from pony import orm

from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.budget import Budget

class BudgetRepository(SqliteRepository[Budget]):
    def __init__(self, filename: str = ':memory:') -> None:
        super().__init__(filename)
        with orm.db_session():
            self._create_budget_initial_entry(1, 100)
            self._create_budget_initial_entry(2, 1000)
            self._create_budget_initial_entry(3, 10000)


    def _create_budget_initial_entry(self, pk, amount):
        b = Budget.get(pk=pk)
        if b == None:
            b0 = Budget(pk=pk, start = datetime.now(), expiration = datetime.now(), amount=amount)

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

    def deleteALL(self):
        with orm.db_session:
            orm.delete(obj for obj in Budget if obj.pk > 3)