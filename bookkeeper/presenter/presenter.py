"""
This module defines the Presenter class, which acts as an intermediary between the UI and repositories.
It handles logic of the application, such as managing categories, expenses, and budgets.

Classes:
    Presenter: Intermediary class between UI and repositories.

Signals:
    updatedCategory: Signal emitted when category data is updated.
    updatedExpense: Signal emitted when expense data is updated.
    updatedBudget: Signal emitted when budget data is updated.

Usage:
    # Example usage of Presenter
    presenter = Presenter()
    presenter.addCategory("Food")
    presenter.commitCategories()
    presenter.addExpense("Food", 50, datetime.datetime.now())
    presenter.addBudget(datetime.datetime.now(), datetime.datetime.now(), 100, 1)
    presenter.commitBudget()
"""
import datetime

from pony import orm
from PySide6.QtCore import QObject, Signal
from typing import Any

from bookkeeper.repository.budget_repository import BudgetRepository
from bookkeeper.repository.category_repository import CategoryRepository
from bookkeeper.repository.expense_repository import ExpenseRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

class Presenter(QObject):

    """
    Intermediary class between UI and repositories.
    Handles logic of the application such as managing categories, expenses, and budgets.

    Attributes:
        _budgetRepo (BudgetRepository): Repository for managing budgets.
        _categoryRepo (CategoryRepository): Repository for managing categories.
        _expenseRepo (ExpenseRepository): Repository for managing expenses.
        updatedCategory (Signal): Signal emitted when category data is updated.
        updatedExpense (Signal): Signal emitted when expense data is updated.
        updatedBudget (Signal): Signal emitted when budget data is updated.
    """

    _budgetRepo: BudgetRepository
    _categoryRepo: CategoryRepository
    _expenseRepo: ExpenseRepository

    updatedCategory: Signal = Signal(bool)
    updatedExpense: Signal = Signal(bool)
    updatedBudget: Signal = Signal(bool)

    _pendingCategoryChanges: list[list[str]] = []
    _pendingBudgetChanges: list[list[Any]] = []

    _budget_Idprim_keyDict: dict[int, int] = {}

    def __init__(self, name: str = ':memory:') -> None:
        """
        Initializes Presenter object with repositories.

        Args:
            name (str): Name of the database file. Defaults to in-memory database.
        """
        super().__init__()
        self._budgetRepo = BudgetRepository(name)
        self._categoryRepo = CategoryRepository(name)
        self._expenseRepo = ExpenseRepository(name)

    def _getCategoryChildren(self, item: str) -> dict[str, list[str]]:
        """
        Recursively traverses database and appends children of categories to the result dictionary.

        Args:
            item (str): Name of the parent category.

        Returns:
            dict: Dictionary containing parent category names as keys and their children as values.
        """
        res: dict[str, list[str]] = {}
        parentCat = self._categoryRepo.get_by_name(item)
        children = [x.name for x in self._categoryRepo.get_all(lambda x: x.parent == parentCat.prim_key)]
        for child in children:
            next_children = self._getCategoryChildren(child)
            if len(next_children) != 0:
                #TODO extract function from following:
                res = dict(list(res.items()) + list(next_children.items()))
                #TODO extract function from following:
        return dict(list({item: children}.items()) + list(res.items()))

# TODO replace cat[0], ... with class change

    def _removeCategory(self, cat: str, topLevels: list[str], res: dict[str, list[str]]) -> None:
        """
        Removes a category and its children from the result dictionary.

        Args:
            cat (str): Name of the category to remove.
            topLevels (list[str]): List of top-level categories.
            res (dict): Dictionary containing category hierarchy.
        """
        if cat[0] in topLevels: topLevels.remove(cat[0])
        # Remember entry, for which the removed list is a parent
        # and rebind to parent of removed list
        for key, lst in res.items():
            if cat[0] in lst:
                lst.remove(cat[0])
                parent = key
        for key in res.keys():
            if key == cat[0]:
                res[parent] += res[key]
                del res[key]

    def getCategoriesHierarchy(self) -> tuple[list[str], dict[str, list[str]]]:
        """
        Retrieves the hierarchy of categories from the database.

        Returns:
            tuple: Tuple containing a list of top-level categories and a dictionary representing category hierarchy.
        """
        with orm.db_session():
            topLevels = [x.name for x in self._categoryRepo.get_all(lambda x: x.parent == None)]
            res: dict[str, list[str]] = {}
            for item in topLevels:
                #TODO extract function from following:
                res = dict(list(res.items()) + list(self._getCategoryChildren(item).items()))

        # After collection we need to apply changes, if any
        for cat in self._pendingCategoryChanges:
            if cat[0] == None:
                # Add new category
                if cat[2]!=None:
                    res[cat[2]]+=[cat[1]]
                else:
                    topLevels+={cat[1]}
                res[cat[1]]=[]
            elif cat[1] == None:
                self._removeCategory(cat, topLevels, res)
            else:
                # Rename category
                if cat[0] in topLevels: topLevels.remove(cat[0])
                for lst in res.items():
                    if cat[0] in lst: lst.remove(cat[0])
        return topLevels, res

    def getAllCategories(self) -> list[str]:
        """
        Retrieves all categories from the database.

        Returns:
            list: List of category names.
        """
        return self.getCategoriesHierarchy()[1].keys()

    def addCategory(self, cat: str, parent = None) -> None:
        """
        Adds a new category to the database.

        Args:
            cat (str): Name of the category to add.
            parent (str, optional): Parent category. Defaults to None.
        """
        if self._categoryRepo.get_by_name(cat) != None:
            raise RuntimeError('Entry already exists!')
        self._pendingCategoryChanges.append([None, cat, parent])
        self.updatedCategory.emit(True)

    def commitCategories(self) -> None:
        """
        Saves pending category changes.
        """
        with orm.db_session:
            for cat in self._pendingCategoryChanges:
                if cat[0] == None:
                    # Add new category
                    if cat[2]==None:
                        self._categoryRepo.add(Category(name=cat[1]))
                    else:
                        parentCatprim_key=self._categoryRepo.get_by_name(cat[2]).prim_key
                        self._categoryRepo.add(Category(name=cat[1], parent=parentCatprim_key))
                elif cat[1] == None:
                    # Remove category: rebind children to elder parent
                    currentCat = Category(name=cat[0])
                    for child in self._categoryRepo.get_all(lambda x: x.parent==currentCat.prim_key):
                        child.parent = currentCat.parent
                        self._categoryRepo.update(child)
                    self._categoryRepo.delete(currentCat.prim_key)
                else:
                    # Update category
                    # TODO check for wrong naming
                    c = Category(name=cat[0])
                    c.name = cat[1]
                    c.parent = Category(name=cat[2]).prim_key
                    self._categoryRepo.update(c)
        self._pendingCategoryChanges = []

    def cancelCategories(self) -> None:
        """
        Cancels pending category changes.
        """
        self._pendingCategoryChanges = []

    def addExpense(self, category: str, value: int, dt: datetime.datetime, comment: str = '') -> None:
        """
        Adds a new expense to the database.

        Args:
            category (str): Category of the expense.
            value (int): Amount of the expense.
            dt (datetime.datetime): Date and time of the expense.
            comment (str, optional): Additional comment for the expense. Defaults to ''.
        """
        with orm.db_session():
            catEntry = self._categoryRepo.get_by_name(category)
            if comment == '':
                exp = Expense(amount=value, category=catEntry, expense_date=dt)
            else:
                exp = Expense(amount=value, category=catEntry, expense_date=dt, comment=comment)
            self._expenseRepo.add(exp)
        self.updatedExpense.emit(True)

#TODO replace list with tuple or with class object
    def getExpensesInInterval(self, begin: datetime.date, end: datetime.date)-> list[list[Any]]:
        """
        Retrieves expenses within the specified date range from the database.

        Args:
            begin (datetime.date): Start date of the interval.
            end (datetime.date): End date of the interval.

        Returns:
            list: List of expenses within the specified date range.
        """
        beginDT = self.getDateTime_fromDate(begin)
        endDT = self.getDateTime_fromDate(end, ceil=False)
        with orm.db_session():
            res = self._expenseRepo.get_all(lambda x: x.expense_date <= endDT and x.expense_date >= beginDT)
            return [[item.expense_date, item.amount, item.category.name, item.comment] for item in res]

# TODO remove datetime.datetime
    def getRecentExpenses(self, days: int)-> list[list[datetime.datetime, int, str, str]]:
        """
        Retrieves recent expenses from the database.

        Args:
            days (int): Number of days to consider for recent expenses.

        Returns:
            list: List of recent expenses.
        """
        return self.getExpensesInInterval(datetime.datetime.now()-datetime.timedelta(days=days), datetime.datetime.now())

    def getBudgets(self):
        """
        Retrieves budgets from the database.

        Returns:
            list: List of budgets.
        """
        # We need to combine data stored in database with current uncommited changes
        with orm.db_session():
            res = self._budgetRepo.get_all(lambda x: x.prim_key > 3)
            for i in range(len(res)):
                self._budget_Idprim_keyDict[i+3] = res[i].prim_key
            currentBudgets = [[item.start, item.expiration, item.amount, k+3] for k, item in enumerate(res)]
        # The budget indexes which were affected by change
        changedIndexes = [i[3] for i in self._pendingBudgetChanges]

        # replace budgets from database with local changes and append
        for i, budget in enumerate(currentBudgets):
            if budget[3] in changedIndexes:
                indexToRemove = changedIndexes.index(budget[3])
                currentBudgets[i] = self._pendingBudgetChanges[indexToRemove]
                del changedIndexes[indexToRemove]
        for i in changedIndexes:
            if i >= 3:
                item = next(filter(lambda x: x[3]==i, self._pendingBudgetChanges), None)
                currentBudgets.append(item)
        return currentBudgets

    def getBudget(self, period: int):
        """
        Retrieves budget for the specified period from the database.

        Args:
            period (int): Period for which budget is requested (1=daily, 2=weekly, 3=monthly).

        Returns:
            int: Budget amount for the specified period.
        """
        changedIndexes = [i[3] for i in self._pendingBudgetChanges]
        if period-1 in changedIndexes:
            return self._pendingBudgetChanges[changedIndexes.index(period-1)][2]
        with orm.db_session():
            res = self._budgetRepo.get(period)
            self._budget_Idprim_keyDict[period-1] = res.prim_key
            return res.amount

    def addBudget(self, start: datetime.datetime, end: datetime.datetime, plan: int, index: int):
        """
        Adds or updates a budget entry in the database.

        Args:
            start (datetime.datetime): Start date and time of the budget period.
            end (datetime.datetime): End date and time of the budget period.
            plan (int): Planned budget amount.
            index (int): Index of the budget entry.
        """
        self._pendingBudgetChanges.append([start, end, plan, index])
        self.updatedBudget.emit(True)

    def updateBudget(self, index: int, plan: int):
        """
        Updates the budget plan for the specified index.

        Args:
            index (int): Index of the budget entry.
            plan (int): New planned budget amount.
        """
        try:
            budgetEntry = self._budgetRepo.get(self._budget_Idprim_keyDict[index])
            self._pendingBudgetChanges.append([budgetEntry.start, budgetEntry.expiration, plan, index])
        except KeyError:
            #TODO move to function:
            item = next(filter(lambda x: x[3]==index, self._pendingBudgetChanges), None)
            item[2] = plan
        self.updatedBudget.emit(True)

#TODO move to utils
    def getDateTime_fromDate(self, date: datetime.date, ceil: bool = True) -> datetime.datetime:
        """
        Converts a date object to a datetime object.

        Args:
            date (datetime.date): Date to be converted.
            ceil (bool, optional): Whether to ceil the datetime object. Defaults to True.

        Returns:
            datetime.datetime: Converted datetime object.
        """
        if ceil:
            return datetime.datetime.combine(date, datetime.datetime.min.time())
        else:
            return datetime.datetime.combine(date, datetime.datetime.max.time())

    #TODO refactor following:
    def commitBudget(self):
        """
        Commits pending budget changes to the database.
        """
        with orm.db_session():
            for budget in self._pendingBudgetChanges:
                if budget[3] != None and not budget[3] in self._budget_Idprim_keyDict.keys():
                    # Append
                    budgetEntry = Budget(start=self.getDateTime_fromDate(budget[0]), expiration=self.getDateTime_fromDate(budget[1]), amount=budget[2])
                    self._budgetRepo.add(budgetEntry)
                    self._budget_Idprim_keyDict[budget[3]] = budgetEntry.prim_key
                elif budget[3] != None and budget[3] in self._budget_Idprim_keyDict.keys():
                    # Update
                    budgetEntry = self._budgetRepo.get(self._budget_Idprim_keyDict[budget[3]])
                    budgetEntry.start = self.getDateTime_fromDate(budget[0])
                    budgetEntry.expiration = datetime.datetime.combine(budget[1], datetime.datetime.min.time())
                    budgetEntry.amount = budget[2]
                    self._budgetRepo.update(budgetEntry)
                elif budget[2]==None:
                    # Remove
                    self._budgetRepo.delete(budget[3])
                else:
                    raise RuntimeError('Budget entry corrupted')
        self._pendingBudgetChanges = []

    def cancelBudget(self):
        """
        Cancels pending budget changes.
        """
        self._pendingBudgetChanges = []

    def delete_all(self):
        """
        Deletes all data from the database.
        """
        with orm.db_session:
            self._budgetRepo.delete_all()
            self._categoryRepo.delete_all()
            self._expenseRepo.delete_all()
        self._pendingCategoryChanges = []
        self._pendingBudgetChanges = []