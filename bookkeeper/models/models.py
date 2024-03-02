"""The file `models.py` describes all the models, used in application. 

All the models were defined in single file because the database
must be created and bound before any changes. 
Generally, this is only approach, shown in PonyORM docs.
See the docs [here](https://docs.ponyorm.org/database.html)
"""

from datetime import datetime
import pony.orm as orm

db = orm.Database()

class Category(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    parent = orm.Optional(int)

class Expence(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    category = orm.Required('Category')
    expence_date = orm.Required(datetime)
    added_date = orm.Required(datetime)
    comment = orm.Optional(str)

class Budget(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    start = orm.Required(datetime)
    expiration = orm.Required(datetime)
    amount = orm.Required(int)