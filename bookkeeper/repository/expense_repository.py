from pony import orm
from typing import Callable

from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.expense import Expense

class ExpenseRepository(SqliteRepository[Expense]):
    def __init__(self, filename=':memory:') -> None:
        super().__init__(filename)

    def add(self, obj: Expense) -> int:
        with orm.db_session:
            instance = obj
            orm.commit()
            return instance.pk

    def get(self, pk: int)-> Any:
        with orm.db_session:
            return Expense.get(pk=pk)
    
    def get_all(self, where: Callable[[Any], bool] = True) -> Any:
        with orm.db_session:
            if where is True:
                return orm.select(obj for obj in Expense)[:]
            return orm.select(obj for obj in Expense if where(obj))[:]
        
    def update(self, obj: Expense) -> None:
        with orm.db_session:
            orm.commit()

    def delete(self, pk: int) -> None:
        with orm.db_session:
            Expense[pk].delete()