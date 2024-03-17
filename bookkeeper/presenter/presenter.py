import datetime

from pony import orm
from PySide6.QtCore import QObject, Signal

from bookkeeper.repository.budget_repository import BudgetRepository
from bookkeeper.repository.category_repository import CategoryRepository
from bookkeeper.repository.expense_repository import ExpenseRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

class Presenter(QObject):
    _budgetRepo: BudgetRepository
    _categoryRepo: CategoryRepository
    _expenseRepo: ExpenseRepository

    updatedCategory: Signal = Signal(bool)
    updatedExpense: Signal = Signal(bool)
    updatedBudget: Signal = Signal(bool)

    _pendingCategoryChanges = []
    _pendingBudgetChanges = []

    _budget_IdPkDict = {}

    def __init__(self) -> None:
        super().__init__()
        self._budgetRepo = BudgetRepository('data.db3')
        self._categoryRepo = CategoryRepository('data.db3')
        self._expenseRepo = ExpenseRepository('data.db3')

    def _getCategoryChildren(self, item):
        # Recursively traverse database and append res, which is dictionary {parent: [children]}
        res = {}
        parentCat = self._categoryRepo.getByName(item)
        children = [x.name for x in self._categoryRepo.get_all(lambda x: x.parent == parentCat.pk)]
        for child in children:
            next_children = self._getCategoryChildren(child)
            if len(next_children) != 0:
                #TODO extract function from following:
                res = dict(list(res.items()) + list(next_children.items()))
                #TODO extract function from following:
        return dict(list({item: children}.items()) + list(res.items()))

# TODO replace cat[0], ... with class change

    def _removeCategory(self, cat, topLevels, res):
        # Remove category
        if cat[0] in topLevels: topLevels.remove(cat[0])
        # Remember entry, for which the removed list is a parent
        # and rebind to parent of removed list
        for key, lst in res:
            if cat[0] in lst:
                lst.remove(cat[0])
                parent = key
        for key in res.keys():
            if key == cat[0]:
                res[parent] += res[key]
                del res[key]
                
    def getCategoriesHierarchy(self):
        with orm.db_session():
            topLevels = [x.name for x in self._categoryRepo.get_all(lambda x: x.parent == None)]
            res = {}
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
    
    def getAllCategories(self):
        return self.getCategoriesHierarchy()[1].keys()

    def addCategory(self, cat: str, parent = None):
        if self._categoryRepo.getByName(cat) != None:
            raise RuntimeError('Entry already exists!')
        self._pendingCategoryChanges.append([None, cat, parent])
        self.updatedCategory.emit(True)

    def commitCategories(self):
        with orm.db_session:
            for cat in self._pendingCategoryChanges:
                if cat[0] == None:
                    # Add new category
                    if cat[2]==None:
                        self._categoryRepo.add(Category(name=cat[1]))    
                    else:
                        parentCatPk=self._categoryRepo.getByName(cat[2]).pk
                        self._categoryRepo.add(Category(name=cat[1], parent=parentCatPk))
                elif cat[1] == None:
                    # Remove category: rebind children to elder perent
                    currentCat = Category(name=cat[0])
                    for child in self._categoryRepo.get_all(lambda x: x.parent==currentCat.pk):
                        child.parent = currentCat.parent
                        self._categoryRepo.update(child)
                    self._categoryRepo.delete()
                else:
                    # Update category
                    # TODO check for wrong naming
                    c = Category(name=cat[0])
                    c.name = cat[1]
                    c.parent = Category(name=cat[2]).pk
                    self._categoryRepo.update(c)
        self._pendingCategoryChanges = []
    
    def cancelCategories(self):
        self._pendingCategoryChanges = []

    def addExpense(self, category: str, value: int, dt: datetime.datetime, comment: str = None):
        with orm.db_session():
            catEntry = self._categoryRepo.getByName(category)
            if comment == None:
                exp = Expense(amount=value, category=catEntry, expense_date=dt)
            else:
                exp = Expense(amount=value, category=catEntry, expense_date=dt, comment=comment)
            self._expenseRepo.add(exp)
        self.updatedExpense.emit(True)

    def getExpensesInInterval(self, begin: datetime.datetime, end: datetime.datetime):
        with orm.db_session():
            res = self._expenseRepo.get_all(lambda x: x.expense_date < end and x.expense_date >= begin)
            return [[item.expense_date, item.amount, item.category.name, item.comment] for item in res]

# TODO remove datetime.datetime
    def getRecentExpenses(self, days: int):
        return self.getExpensesInInterval(datetime.datetime.now()-datetime.timedelta(days=days), datetime.datetime.now())

    def getBudgets(self):
        with orm.db_session():
            res = self._budgetRepo.get_all(lambda x: x.pk > 3)
            for i in range(len(res)):
                self._budget_IdPkDict[i] = res[i].pk
            _currentBudgets = [[item.start, item.expiration, item.amount, None] for item in res] + self._pendingBudgetChanges
            return _currentBudgets
        
    # 1=daily, 2=weekly, 3=monthly
    def getBudget(self, period: int):
        with orm.db_session():
            res = self._budgetRepo.get(period)
            self._budget_IdPkDict[period-1] = res.pk
            return res.amount
        
    def addBudget(self, start: datetime.datetime, end: datetime.datetime, plan: int, index: int):
        self._pendingBudgetChanges.append([start, end, plan, index])
        self.updatedBudget.emit(True)

#TODO move to utils
    def getDateTime_fromDate(self, date):
        return datetime.datetime.combine(date, datetime.datetime.min.time())

    #TODO refactor following:
    def commitBudget(self):
        with orm.db_session():
            for budget in self._pendingBudgetChanges:
                if budget[3] != None and not budget[3] in self._budget_IdPkDict.keys():
                    # Append
                    budgetEntry = Budget(start=self.getDateTime_fromDate(budget[0]), expiration=self.getDateTime_fromDate(budget[1]), amount=budget[2])
                    self._budgetRepo.add(budgetEntry)
                    self._budget_IdPkDict[budget[3]] = budgetEntry.pk
                elif budget[3] != None and budget[3] in self._budget_IdPkDict.keys():
                    # Update
                    budgetEntry = self._budgetRepo.get(self._budget_IdPkDict[budget[3]])
                    budgetEntry.start = self.getDateTime_fromDate(budget)
                    budgetEntry.expiration = datetime.datetime.combine(budget[1], datetime.datetime.min.time())
                    budgetEntry.amount = budget[2]
                    self._budgetRepo.update(budgetEntry)
                elif budget[2]==None:
                    # Remove
                    self._budgetRepo.delete(budget[3])
                else:
                    raise RuntimeError('Budget entry corrupted')
        self._pendingBudgetChanges

    def cancelBudget(self):
        self._pendingBudgetChanges = []