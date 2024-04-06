from pony import orm
from typing import Callable, Any

from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.category import Category

class CategoryRepository(SqliteRepository[Category]):
    def __init__(self, filename: str = ':memory:') -> None:
        super().__init__(filename)

    def add(self, obj: Category) -> int:
        with orm.db_session:
            instance = obj
            orm.commit()
            return instance.pk

    
    def get(self, pk: int)-> Any:
        with orm.db_session:
            return Category.get(pk=pk)
    
    
    def getByName(self, name: str) -> Any:
        with orm.db_session:
            return Category.get(name=name)

    
    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> Any:
        with orm.db_session:
            return orm.select(obj for obj in Category if where(obj))[:]

    
    def update(self, obj: Category) -> None:
        with orm.db_session:
            orm.commit()

    
    def delete(self, pk: int) -> None:
        with orm.db_session:
            Category[pk].delete()

    def deleteALL(self):
        with orm.db_session:
            orm.delete(obj for obj in Category)