from datetime import datetime

from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.budget import Budget

class BudgetRepository(SqliteRepository[T]):
    def __init__(self, filename=':memory:') -> None:
        super().__init__(filename)
        with orm.db_session():
            try:
                b = Budget[1]
            except orm.ObjectNotFound:
                # Initialize daily, weekly, monthly
                b0 = Budget(start = datetime.now(), expiration = datetime.now(), amount=100)
                b1 = Budget(start = datetime.now(), expiration = datetime.now(), amount=1000)
                b2 = Budget(start = datetime.now(), expiration = datetime.now(), amount=10000)

    @orm.db_session
    def add(self, obj: Budget) -> int:
        instance = obj
        orm.commit()
        return instance.pk

    @orm.db_session
    def get(self, pk: int)-> Budget:
        return Budget[pk]
    
    @orm.db_session
    def get_all(self, where = None) -> list[Budget]:
        if where is None:
            return orm.select(obj for obj in Budget)[:]
        return orm.select(obj for obj in Budget if where(obj))[:]
        
    @orm.db_session
    def update(self, obj: Budget) -> None:
        orm.commit()

    @orm.db_session
    def delete(self, pk: int) -> None:
        Budget[pk].delete()