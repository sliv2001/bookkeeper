from pony import orm
from datetime import datetime

from bookkeeper.models.database import db
from bookkeeper.models.category import Category

class Expense(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    # category = orm.Required(Category)
    expence_date = orm.Required(datetime)
    added_date = orm.Required(datetime)
    comment = orm.Optional(str)