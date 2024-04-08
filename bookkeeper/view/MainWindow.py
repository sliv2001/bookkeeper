from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QTableWidgetItem

from bookkeeper.view.Ui_MainWindow import Ui_MainWindow
from bookkeeper.view.Budget import BudgetView
from bookkeeper.view.AddUpdateDialog import AddUpdateDialog
from bookkeeper.view.Category import CategoryDialog
from bookkeeper.presenter.presenter import Presenter


class MainWindow(QMainWindow):
    """
    Main window of the application.

    Attributes:
        ui (QMainWindow): Main window UI.
        budgetView (BudgetView): Budget view dialog.
        addUpdateView (AddUpdateDialog): Add/update expense dialog.
        categoryView (CategoryDialog): Category management dialog.
        presenter (Presenter): Presenter object.
    """

    ui: QMainWindow
    budgetView: BudgetView
    addUpdateView: AddUpdateDialog
    categoryView: CategoryDialog
    presenter: Presenter

    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        """
        Initializes the MainWindow.

        Args:
            parent (QWidget | None, optional): Parent widget. Defaults to ... (None).
            flags (Qt.WindowType, optional): Window flags. Defaults to Qt.WindowType.
        """
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.presenter = Presenter(name='data.db3')
        self.presenter.updatedExpense.connect(self.updateMainView)
        self.updateMainView()

    @Slot()
    def on_actionAddOperation_triggered(self) -> None:
        """
        Slot handling the trigger of the 'Add Operation' action.
        """
        self.addUpdateView = AddUpdateDialog(parent=self)
        self.addUpdateView.show()

    @Slot()
    def on_actionShowBudget_triggered(self) -> None:
        """
        Slot handling the trigger of the 'Show Budget' action.
        """
        self.budgetView = BudgetView(parent=self)
        self.budgetView.show()

    @Slot()
    def on_actionAlterCats_triggered(self) -> None:
        """
        Slot handling the trigger of the 'Alter Categories' action.
        """
        self.categoryView = CategoryDialog(parent=self)
        self.categoryView.show()

    @Slot()
    def updateMainView(self) -> None:
        """
        Update the main view with recent expenses.
        """
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

        self.ui.summary.setText('Итого: ' + str(res) +
                                '₽ за последние ' + str(days) + ' дней')
