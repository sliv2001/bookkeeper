from pony import orm

from bookkeeper.repository.budget_repository import BudgetRepository
from bookkeeper.repository.category_repository import CategoryRepository
from bookkeeper.repository.expense_repository import ExpenseRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

class Presenter:
    budgetModel: BudgetRepository
    categoryModel: CategoryRepository
    expenseModel: ExpenseRepository

    def __init__(self) -> None:
        self.budgetModel = BudgetRepository('data.db3')
        self.categoryModel = CategoryRepository('data.db3')
        self.expenseModel = ExpenseRepository('data.db3')

    def addCategory(self, cat: str):
        with orm.db_session:
            self.categoryModel.add(Category(name=cat))