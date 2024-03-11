from bookkeeper.repository.budget_repository import BudgetRepository
from bookkeeper.repository.category_repository import CategoryRepository
from bookkeeper.repository.expense_repository import ExpenseRepository

class Presenter:
    budgetModel: BudgetRepository
    categoryModel: CategoryRepository
    expenseModel: ExpenseRepository

    def __init__(self) -> None:
        self.budgetModel = BudgetRepository('data.db3')
        self.categoryModel = CategoryRepository('data.db3')
        self.expenseModel = ExpenseRepository('data.db3')
