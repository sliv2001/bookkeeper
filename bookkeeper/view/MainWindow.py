from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QMessageBox, QDialog
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

    @Slot()
    def on_actionAddOperation_triggered(self):
        self.addUpdateView = AddUpdateDialog()
        self.addUpdateView.show()

    @Slot()
    def on_actionShowBudget_triggered(self):
        self.budgetView = BudgetView()
        self.budgetView.show()

    @Slot()
    def on_actionAlterCats_triggered(self):
        self.categoryView = CategoryDialog()
        self.categoryView.show()
