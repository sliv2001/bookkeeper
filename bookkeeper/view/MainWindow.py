from datetime import datetime

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QMessageBox, QDialog, QTableWidgetItem, QTableWidget
from PySide6.QtGui import QAction

from bookkeeper.view.Ui_MainWindow import Ui_MainWindow
from bookkeeper.view.Budget import BudgetView
from bookkeeper.view.AddUpdateDialog import AddUpdateDialog
from bookkeeper.view.Category import CategoryDialog
from bookkeeper.presenter.presenter import Presenter

class MainWindow(QMainWindow):

    ui: QMainWindow
    budgetView: BudgetView
    addUpdateView: AddUpdateDialog
    categoryView: CategoryDialog
    presenter: Presenter

    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.presenter = Presenter()
        self.presenter.updatedExpense.connect(self.updateMainView)
        self.updateMainView()

    @Slot()
    def on_actionAddOperation_triggered(self):
        self.addUpdateView = AddUpdateDialog(parent=self)
        self.addUpdateView.show()

    @Slot()
    def on_actionShowBudget_triggered(self):
        self.budgetView = BudgetView(parent=self)
        self.budgetView.show()

    @Slot()
    def on_actionAlterCats_triggered(self):
        self.categoryView = CategoryDialog(parent=self)
        self.categoryView.show()

#TODO replace list with class
    @Slot()
    def updateMainView(self):
        days = 365
        res = 0
        entries = self.presenter.getRecentExpenses(days)
        self.ui.tableWidget.setRowCount(len(entries))
        for i, item in enumerate(entries):
            # The code cannot be unified as format is different
            dt = QTableWidgetItem(item[0].strftime('%a %d %b %Y, %H:%M'))
            exp = QTableWidgetItem(str(item[1]))
            cat = QTableWidgetItem(item[2])
            comment = QTableWidgetItem(item[3])
            dt.setFlags(~Qt.ItemFlag.ItemIsEditable)
            exp.setFlags(~Qt.ItemFlag.ItemIsEditable)
            cat.setFlags(~Qt.ItemFlag.ItemIsEditable)
            comment.setFlags(~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(i, 0, dt)
            self.ui.tableWidget.setItem(i, 1, exp)
            self.ui.tableWidget.setItem(i, 2, cat)
            self.ui.tableWidget.setItem(i, 3, comment)

            res += item[1]
            
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

        self.ui.summary.setText('Итого: ' + str(res) + '₽ за последние ' + str(days) +' дней')
