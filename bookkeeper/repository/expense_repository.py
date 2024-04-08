from pony import orm
from typing import Callable, Any

from bookkeeper.repository.sqlite_repository import *
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
            return instance.pk

    def get(self, pk: int)-> Any:
        """
        Retrieves an Expense object from the database by its primary key.

        Args:
            pk (int): Primary key of the Expense object.

        Returns:
            Any: Expense object corresponding to the primary key.
        """
        with orm.db_session:
            return Expense.get(pk=pk)

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

    def delete(self, pk: int) -> None:
        """
        Deletes an Expense object from the database by its primary key.

        Args:
            pk (int): Primary key of the Expense object to be deleted.
        """
        with orm.db_session:
            Expense[pk].delete()

    def deleteALL(self):
        """
        Deletes all Expense objects from the database.
        """
        with orm.db_session:
            orm.delete(obj for obj in Expense)
