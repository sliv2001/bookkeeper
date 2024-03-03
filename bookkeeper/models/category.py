from pony import orm
from datetime import datetime

from bookkeeper.models.database import db

class Category(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    parent = orm.Optional(int)