"""
This module defines model of budget data in PonyORM-compatible style.

Classes:
    Budget: defines table entries of a budget

    Usage: this is utility class used within budgetRepo
"""
from pony import orm
from datetime import datetime

from bookkeeper.models.database import db

class Budget(db.Entity):

    """
    Primary Key
    """
    prim_key = orm.PrimaryKey(int, auto=True)

    """
    Date/time of beginning of a budget calculation
    """
    start = orm.Required(datetime, default=datetime.now())

    """
    Date/time of ending of a budget calculation
    """
    expiration = orm.Required(datetime)

    """
    Amount of money a user can spend
    """
    amount = orm.Required(int)