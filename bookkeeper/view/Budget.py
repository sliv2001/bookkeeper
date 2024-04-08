from datetime import datetime, timedelta
from dateutil import relativedelta

from PySide6.QtCore import Qt, Slot, QDateTime
from PySide6.QtWidgets import QDialog, QWidget, QTableWidgetItem
from PySide6.QtGui import QColor

from bookkeeper.view.Ui_Budget import Ui_BudgetWindow
from bookkeeper.presenter.presenter import Presenter


class BudgetView(QDialog):
    """
    Dialog for managing budget entries.

    Args:
        presenter (Presenter, optional): Presenter object. Defaults to None.
        parent (QWidget | None, optional): Parent widget. Defaults to ... (None).
        flags (Qt.WindowType, optional): Window flags. Defaults to Qt.WindowType.
    """

    _presenter: Presenter

    _updateAllowed: bool = False

    def __init__(self, presenter: Presenter = None,
                 parent: QWidget | None = ...) -> None:
        """
        Initializes the BudgetView dialog.

        Args:
            presenter (Presenter, optional): Presenter object. Defaults to None.
            parent (QWidget | None, optional): Parent widget. Defaults to ... (None).
            flags (Qt.WindowType, optional): Window flags. Defaults to Qt.WindowType.
        """
        super(BudgetView, self).__init__()
        if presenter is None:
            self._presenter = parent.presenter
        else:
            self._presenter = presenter
        self.ui = Ui_BudgetWindow()
        self.ui.setupUi(self)
        self.ui.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateEdit_2.setDateTime(QDateTime.currentDateTime())
        self.updateBudget()
        self._updateAllowed = True
        self._presenter.updatedBudget.connect(self.updateBudget)

    @Slot()
    def on_pushButton_clicked(self):
        """
        Slot handling the click event of the push button.
        """
        dateStart = self.ui.dateEdit.date().toPython()
        dateEnd = self.ui.dateEdit_2.date().toPython()
        if (dateStart > dateEnd):
            raise RuntimeWarning('Starting time cannot be greater than ending time')
        else:
            self._presenter.addBudget(  dateStart,
                                        dateEnd,
                                        self.ui.spinBox.value(),
                                        self.ui.tableWidget.rowCount())

    @Slot()
    def accept(self) -> None:
        """
        Slot handling the acceptance of the dialog.
        """
        self._presenter.commitBudget()
        return super().accept()

    @Slot()
    def reject(self) -> None:
        """
        Slot handling the rejection of the dialog.
        """
        self._presenter.cancelBudget()
        return super().reject()

    @Slot()
    def on_spinBox_textChanged(self):
        """
        Slot handling the change in spin box text.
        """
        self.updateAddButton()

    @Slot(QTableWidgetItem)
    def on_tableWidget_itemChanged(self, item: QTableWidgetItem):
        """
        Slot handling the change in table widget item.
        """
        if self._updateAllowed and item.column() == 2:
            self._presenter.updateBudget(item.row(), int(item.text()))

    def appendBudgetEntry(self, index: int, start: datetime, end: datetime, plan: int):
        """
        Append a budget entry to the table widget.

        Args:
            index (int): Row index.
            start (datetime): Start date and time.
            end (datetime): End date and time.
            plan (int): Planned budget amount.
        """
        self._updateAllowed = False
        entryStart = QTableWidgetItem(start.strftime('%a %d %b %Y'))
        entryStart.setFlags(~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(index, 0, entryStart)
        entryEnd = QTableWidgetItem(end.strftime('%a %d %b %Y'))
        entryEnd.setFlags(~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(index, 1, entryEnd)
        entryPlan = QTableWidgetItem(str(plan))
        self.ui.tableWidget.setItem(index, 2, entryPlan)

        expenseList = [int(amount[1]) for amount in
                       self._presenter.getExpensesInInterval(start, end)]
        expenses = sum(expenseList)
        entrySlack = QTableWidgetItem(str(plan-expenses))
        entrySlack.setFlags(~Qt.ItemFlag.ItemIsEditable)
        if (plan-expenses < 0):
            entrySlack.setBackground(QColor('red'))
        self.ui.tableWidget.setItem(index, 3, entrySlack)
        self._updateAllowed = True

    def getWeekBorders(self, dt: datetime):
        """
        Get the start and end dates of the week containing the given date.

        Args:
            dt (datetime): Date.

        Returns:
            Tuple[datetime, datetime]: Start and end dates of the week.
        """
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        return start, end

    def getMonthBorders(self, dt: datetime):
        """
        Get the start and end dates of the month containing the given date.

        Args:
            dt (datetime): Date.

        Returns:
            Tuple[datetime, datetime]: Start and end dates of the month.
        """
        start = dt + relativedelta.relativedelta(day=1)
        end = dt + relativedelta.relativedelta(day=31)
        return start, end

    @Slot()
    def updateBudget(self):
        """
        Update the budget information in the dialog.
        """
        entries = self._presenter.getBudgets()
        self.ui.tableWidget.setRowCount(len(entries)+3)

        self.appendBudgetEntry(0, datetime.today(),
                               datetime.today(),
                               self._presenter.getBudget(1))

        # TODO move these to utils
        weekBegin, weekEnd = self.getWeekBorders(datetime.now())
        self.appendBudgetEntry(1, weekBegin, weekEnd, self._presenter.getBudget(2))

        monthBegin, monthEnd = self.getMonthBorders(datetime.now())
        self.appendBudgetEntry(2, monthBegin, monthEnd, self._presenter.getBudget(3))

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

        for i, item in enumerate(entries):
            self.appendBudgetEntry(3+i, item[0], item[1], item[2])

        self.updateAddButton()

    def updateAddButton(self):
        """
        Update the state of the Add button based on input validity.
        """
        self.ui.pushButton.setEnabled(self.ui.spinBox.value() > 0)
