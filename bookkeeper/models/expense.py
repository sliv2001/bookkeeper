from pony import orm
from datetime import datetime

from bookkeeper.models.database import db
from bookkeeper.models.category import Category

class Expense(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    amount = orm.Required(int)
    category = orm.Required(Category)
    expense_date = orm.Required(datetime, default=datetime.now())
    added_date = orm.Required(datetime, default=datetime.now())
    comment = orm.Optional(str)
