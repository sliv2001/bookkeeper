"""
This module describes repository for managing Expense objects in the database.
"""
from typing import Callable, Any
from pony import orm
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.models.expense import Expense


class ExpenseRepository(SqliteRepository[Expense]):
    """
    Repository for managing Expense objects in the database.

    Args:
        filename (str, optional): Filename of the SQLite database. Defaults to ':memory:'.
    """

    def __init__(self, filename: str = ':memory:') -> None:
        """
        Initializes the ExpenseRepository.

        Args:
            filename (str, optional): Filename of the SQLite database. Defaults to ':memory:'.
        """
        super().__init__(filename)

    def add(self, obj: Expense) -> int:
        """
        Adds a new Expense object to the database.

        Args:
            obj (Expense): Expense object to be added.

        Returns:
            int: Primary key of the added object.
        """
        with orm.db_session:
            instance = obj
            orm.commit()
            return instance.prim_key

    def get(self, prim_key: int)-> Any:
        """
        Retrieves an Expense object from the database by its primary key.

        Args:
            prim_key (int): Primary key of the Expense object.

        Returns:
            Any: Expense object corresponding to the primary key.
        """
        with orm.db_session:
            return Expense.get(prim_key=prim_key)

    @orm.db_session
    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> Any:
        """
        Retrieves all Expense objects from the database.

        Args:
            where (Callable[[Any], bool], optional): Filter function. Defaults to lambda x: True.

        Returns:
            Any: List of Expense objects.
        """
        with orm.db_session:
            return orm.select(obj for obj in Expense if where(obj))[:]

    def update(self, obj: Expense) -> None:
        """
        Updates an Expense object in the database.

        Args:
            obj (Expense): Expense object to be updated.
        """
        with orm.db_session:
            orm.commit()

    def delete(self, prim_key: int) -> None:
        """
        Deletes an Expense object from the database by its primary key.

        Args:
            prim_key (int): Primary key of the Expense object to be deleted.
        """
        with orm.db_session:
            Expense[prim_key].delete()

    def delete_all(self):
        """
        Deletes all Expense objects from the database.
        """
        with orm.db_session:
            orm.delete(obj for obj in Expense)
