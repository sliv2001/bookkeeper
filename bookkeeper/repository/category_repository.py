from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.category import Category

class CategoryRepository(SqliteRepository[T]):
    def __init__(self, filename=':memory:') -> None:
        super().__init__(filename)

    @orm.db_session
    def add(self, obj: Category) -> int:
        instance = obj
        orm.commit()
        return instance.pk

    @orm.db_session
    def get(self, pk: int)-> Category:
        return Category[pk]
    
    @orm.db_session
    def getByName(self, name: str) -> Category:
        return Category.get(name=name)

    @orm.db_session
    def get_all(self, where = None) -> list[Category]:
        if where is None:
            return orm.select(obj for obj in Category)[:]
        return orm.select(obj for obj in Category if where(obj))[:]

    @orm.db_session
    def update(self, obj: Category) -> None:
        orm.commit()

    @orm.db_session
    def delete(self, pk: int) -> None:
        Category[pk].delete()