"""
This module defines model of expense data in PonyORM-compatible style.

Classes:
    Expense: defines table entries of a category

    Usage: this is utility class used within expenseRepo
"""
from pony import orm
from datetime import datetime

from bookkeeper.models.database import db
from bookkeeper.models.category import Category

class Expense(db.Entity):

    """
    Primary key.
    """
    pk = orm.PrimaryKey(int, auto=True)

    """
    Amount of money spent within the current expense.
    """
    amount = orm.Required(int)

    """
    External key describing category of expense.
    """
    category = orm.Required(Category)

    """
    Date/Time of expense.
    """
    expense_date = orm.Required(datetime, default=datetime.now())

    """
    Date/Time when expense was added.
    """
    added_date = orm.Required(datetime, default=datetime.now())

    """
    Optional comment.
    """
    comment = orm.Optional(str)
