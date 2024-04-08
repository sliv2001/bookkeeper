"""
The module contains repository for managing Category objects in the database.
"""
from pony import orm
from typing import Callable, Any

from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.models.category import Category

class CategoryRepository(SqliteRepository[Category]):
    """
    Repository for managing Category objects in the database.

    Args:
        filename (str, optional): Filename of the SQLite database. Defaults to ':memory:'.
    """

    def __init__(self, filename: str = ':memory:') -> None:
        """
        Initializes the CategoryRepository.

        Args:
            filename (str, optional): Filename of the SQLite database. Defaults to ':memory:'.
        """
        super().__init__(filename)

    def add(self, obj: Category) -> int:
        """
        Adds a new Category object to the database.

        Args:
            obj (Category): Category object to be added.

        Returns:
            int: Primary key of the added object.
        """
        with orm.db_session:
            instance = obj
            orm.commit()
            return instance.prim_key


    def get(self, prim_key: int)-> Any:
        """
        Retrieves a Category object from the database by its primary key.

        Args:
            prim_key (int): Primary key of the Category object.

        Returns:
            Any: Category object corresponding to the primary key.
        """
        with orm.db_session:
            return Category.get(prim_key=prim_key)


    def get_by_name(self, name: str) -> Any:
        """
        Retrieves a Category object from the database by its name.

        Args:
            name (str): Name of the Category object.

        Returns:
            Any: Category object corresponding to the name.
        """
        with orm.db_session:
            return Category.get(name=name)


    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> Any:
        """
        Retrieves all Category objects from the database.

        Args:
            where (Callable[[Any], bool], optional): Filter function. Defaults to lambda x: True.

        Returns:
            Any: List of Category objects.
        """
        with orm.db_session:
            return orm.select(obj for obj in Category if where(obj))[:]


    def update(self, obj: Category) -> None:
        """
        Updates a Category object in the database.

        Args:
            obj (Category): Category object to be updated.
        """
        with orm.db_session:
            orm.commit()


    def delete(self, prim_key: int) -> None:
        """
        Deletes a Category object from the database by its primary key.

        Args:
            prim_key (int): Primary key of the Category object to be deleted.
        """
        with orm.db_session:
            Category[prim_key].delete()

    def delete_all(self):
        """
        Deletes all Category objects from the database.
        """
        with orm.db_session:
            orm.delete(obj for obj in Category)
