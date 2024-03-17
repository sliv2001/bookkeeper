from datetime import datetime, timedelta
from dateutil import relativedelta

from PySide6.QtCore import Qt, Slot, QDateTime
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtGui import QAction, QColor

from bookkeeper.view.Ui_Budget import Ui_BudgetWindow
from bookkeeper.presenter.presenter import Presenter

class BudgetView(QDialog):

    presenter: Presenter

    def __init__(self, presenter: Presenter = None, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(BudgetView, self).__init__()
        if presenter == None:
            self.presenter = parent.presenter
        else:
            self.presenter = presenter
        self.ui = Ui_BudgetWindow()
        self.ui.setupUi(self)
        self.ui.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateEdit_2.setDateTime(QDateTime.currentDateTime())
        self.presenter.updatedBudget.connect(self.updateBudget)
        self.updateBudget()

    @Slot()
    def on_pushButton_clicked(self):
        self.presenter.addBudget(self.ui.dateEdit.date().toPython(),
                                 self.ui.dateEdit_2.date().toPython(),
                                 self.ui.spinBox.value(),
                                 self.ui.tableWidget.rowCount())

    @Slot()
    def accept(self) -> None:
        self.presenter.commitBudget()
        return super().accept()

    @Slot()
    def reject(self) -> None:
        self.presenter.cancelBudget()
        return super().reject()
    
    @Slot()
    def on_spinBox_textChanged(self):
        self.updateAddButton()

    def appendBudgetEntry(self, index: int, start: datetime, end: datetime, plan: int):
        entryStart = QTableWidgetItem(start.strftime('%a %d %b %Y'))
        entryStart.setFlags(~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(index, 0, entryStart)
        entryEnd = QTableWidgetItem(end.strftime('%a %d %b %Y'))
        entryEnd.setFlags(~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(index, 1, entryEnd)
        entryPlan = QTableWidgetItem(str(plan))
        self.ui.tableWidget.setItem(index, 2, entryPlan)

        expenseList = [int(amount[1]) for amount in self.presenter.getExpensesInInterval(start, end)]
        expenses = sum(expenseList)
        entrySlack = QTableWidgetItem(str(plan-expenses))
        entrySlack.setFlags(~Qt.ItemFlag.ItemIsEditable)
        if (plan-expenses < 0):
            entrySlack.setBackground(QColor('red'))
        self.ui.tableWidget.setItem(index, 3, entrySlack)
        

    def getWeekBorders(self, dt: datetime):
        start = dt - timedelta(days = dt.weekday())
        end = start + timedelta(days = 6)
        return start, end
    
    def getMonthBorders(self, dt: datetime):
        start = dt + relativedelta.relativedelta(day=1)
        end = dt + relativedelta.relativedelta(day=31)
        return start, end

    @Slot()
    def updateBudget(self):
        entries = self.presenter.getBudgets()
        self.ui.tableWidget.setRowCount(len(entries)+3)
        
        #TODO make that compact
        self.appendBudgetEntry(0, datetime.today(), datetime.today(), self.presenter.getBudget(1))

        # TODO move these to utils
        weekBegin, weekEnd = self.getWeekBorders(datetime.now())
        self.appendBudgetEntry(1, weekBegin, weekEnd, self.presenter.getBudget(2))

        monthBegin, monthEnd = self.getMonthBorders(datetime.now())
        self.appendBudgetEntry(2, monthBegin, monthEnd, self.presenter.getBudget(3))

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

        for i, item in enumerate(entries):
            self.appendBudgetEntry(3+i, item[0], item[1], item[2])

        self.updateAddButton()

    def updateAddButton(self):
        self.ui.pushButton.setEnabled(self.ui.spinBox.value() > 0)