from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.expense import Expense

class ExpenseRepository(SqliteRepository[T]):
    def __init__(self, filename=':memory:') -> None:
        super().__init__(filename)

    @orm.db_session
    def add(self, obj: Expense) -> int:
        instance = obj
        return instance.pk

    @orm.db_session
    def get(self, pk: int)-> Expense:
        return Expense[pk]
    
    @orm.db_session
    def get_all(self, where: dict[str, Any] | None = None) -> list[Expense]:
        if where is None:
            return orm.select(obj for obj in Expense)[:]
        orm.select(obj for obj in Expense
                   if all(getattr(obj, attr) == value for attr, value in where.items()))[:]
        
    @orm.db_session
    def update(self, obj: Expense) -> None:
        orm.commit()

    @orm.db_session
    def delete(self, pk: int) -> None:
        Expense[pk].delete()