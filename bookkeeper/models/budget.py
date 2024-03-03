from pony import orm
from datetime import datetime

from bookkeeper.models.database import db

class Budget(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    start = orm.Required(datetime, default=datetime.now())
    expiration = orm.Required(datetime)
    amount = orm.Required(int)