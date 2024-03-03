from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.category import Budget

class BudgetRepository(SqliteRepository[T]):
    def __init__(self, filename=':memory:') -> None:
        super().__init__(filename)

    @orm.db_session
    def add(self, obj: Budget) -> int:
        instance = obj
        return instance.pk

    @orm.db_session
    def get(self, pk: int)-> Budget:
        return Budget[pk]
    
    @orm.db_session
    def get_all(self, where: dict[str, Any] | None = None) -> list[Budget]:
        if where is None:
            return orm.select(obj for obj in Budget)[:]
        orm.select(obj for obj in Budget
                   if all(getattr(obj, attr) == value for attr, value in where.items()))[:]
        
    @orm.db_session
    def update(self, obj: Budget) -> None:
        orm.commit()

    @orm.db_session
    def delete(self, pk: int) -> None:
        Budget[pk].delete()