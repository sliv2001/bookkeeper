"""
Простой тестовый скрипт для терминала
"""
from pony import orm

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.utils import read_tree

cat_repo = SqliteRepository[Category]()
exp_repo = SqliteRepository[Expense]()

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

with orm.db_session:
    created: dict[str, Category] = {}
    for child, parent in read_tree(cats):
        cat = Category(name=child, parent=(created[parent].pk if parent is not None else None), )
        cat_repo.add(cat)
        created[child] = cat

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
