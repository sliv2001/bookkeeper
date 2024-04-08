from datetime import datetime
from typing import Callable, Any
from pony import orm

from bookkeeper.repository.sqlite_repository import *
from bookkeeper.models.budget import Budget

class BudgetRepository(SqliteRepository[Budget]):
    """
    Repository for managing Budget objects in the database.

    Args:
        filename (str, optional): Filename of the SQLite database. Defaults to ':memory:'.
    """

    def __init__(self, filename: str = ':memory:') -> None:
        """
        Initializes the BudgetRepository.

        Args:
            filename (str, optional): Filename of the SQLite database. Defaults to ':memory:'.
        """
        super().__init__(filename)
        with orm.db_session():
            self._create_budget_initial_entry(1, 100)
            self._create_budget_initial_entry(2, 1000)
            self._create_budget_initial_entry(3, 10000)

    def _create_budget_initial_entry(self, pk, amount):
        """
        Creates initial entries in the database if they do not exist.

        Args:
            pk (int): Primary key of the entry.
            amount (int): Budget amount.
        """
        b = Budget.get(pk=pk)
        if b == None:
            b0 = Budget(pk=pk, start = datetime.now(), expiration = datetime.now(), amount=amount)

    def add(self, obj: Budget) -> int:
        """
        Adds a new Budget object to the database.

        Args:
            obj (Budget): Budget object to be added.

        Returns:
            int: Primary key of the added object.
        """
        with orm.db_session:
            instance = obj
            orm.commit()
            return instance.pk

    def get(self, pk: int)-> Any:
        """
        Retrieves a Budget object from the database by its primary key.

        Args:
            pk (int): Primary key of the Budget object.

        Returns:
            Any: Budget object corresponding to the primary key.
        """
        with orm.db_session:
            return Budget[pk]

    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> Any:
        """
        Retrieves all Budget objects from the database.

        Args:
            where (Callable[[Any], bool], optional): Filter function. Defaults to lambda x: True.

        Returns:
            Any: List of Budget objects.
        """
        with orm.db_session:
            return orm.select(obj for obj in Budget if where(obj))[:]

    def update(self, obj: Budget) -> None:
        """
        Updates a Budget object in the database.

        Args:
            obj (Budget): Budget object to be updated.
        """
        with orm.db_session:
            orm.commit()

    def delete(self, pk: int) -> None:
        """
        Deletes a Budget object from the database by its primary key.

        Args:
            pk (int): Primary key of the Budget object to be deleted.
        """
        with orm.db_session:
            Budget[pk].delete()

    def deleteALL(self):
        """
        Deletes all Budget objects from the database.
        """
        with orm.db_session:
            orm.delete(obj for obj in Budget if obj.pk > 3)