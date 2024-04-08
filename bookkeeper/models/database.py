"""
This module introduces utility model used as a utility
around the orm-controlled database, providing some
project-wise database settings.
"""

from pony import orm

db = orm.Database()
