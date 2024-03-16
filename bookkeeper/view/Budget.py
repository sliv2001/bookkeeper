from datetime import datetime, timedelta

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtGui import QAction

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
        self.updateBudget()

    @Slot()
    def accept(self) -> None:
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')
        return super().accept()

    @Slot()
    def reject(self) -> None:
        return super().reject()

    @Slot()
    def updateBudget(self):
        entries = self.presenter.getBudgets()
        self.ui.tableWidget.setRowCount(len(entries)+3)
        
        #TODO make that compact
        dailyStart = QTableWidgetItem(datetime.now().strftime('%a %d %b %Y'))
        self.ui.tableWidget.setItem(0, 0, dailyStart)
        dailyStart.setFlags(~Qt.ItemFlag.ItemIsEditable)
        dailyEnd = QTableWidgetItem(datetime.now().strftime('%a %d %b %Y'))
        self.ui.tableWidget.setItem(0, 1, dailyEnd)
        dailyEnd.setFlags(~Qt.ItemFlag.ItemIsEditable)
        dailyPlan = QTableWidgetItem(str(self.presenter.getBudget(1)))
        self.ui.tableWidget.setItem(0, 2, dailyPlan)

        weekStart=datetime.now()-timedelta(days=datetime.now().weekday())
        weekEnd=weekStart + timedelta(days = 6) 
        weeklyStart = QTableWidgetItem((weekStart).strftime('%a %d %b %Y'))
        self.ui.tableWidget.setItem(1, 0, weeklyStart)
        weeklyStart.setFlags(~Qt.ItemFlag.ItemIsEditable)
        weeklyEnd = QTableWidgetItem((weekEnd).strftime('%a %d %b %Y'))
        self.ui.tableWidget.setItem(1, 1, weeklyEnd)
        weeklyEnd.setFlags(~Qt.ItemFlag.ItemIsEditable)
        weeklyPlan = QTableWidgetItem(str(self.presenter.getBudget(2)))
        self.ui.tableWidget.setItem(1, 2, weeklyPlan)

        mounthlyStart = QTableWidgetItem((datetime.now()+timedelta(months=-1)).strftime('%a %d %b %Y'))
        self.ui.tableWidget.setItem(2, 0, mounthlyStart)
        mounthlyStart.setFlags(~Qt.ItemFlag.ItemIsEditable)
        mounthlyEnd = QTableWidgetItem((datetime.now()+timedelta(=1)).strftime('%a %d %b %Y'))
        self.ui.tableWidget.setItem(2, 1, mounthlyEnd)
        mounthlyEnd.setFlags(~Qt.ItemFlag.ItemIsEditable)
        mounthlyPlan = QTableWidgetItem(str(self.presenter.getBudget(3)))
        self.ui.tableWidget.setItem(2, 2, mounthlyPlan)

        for i, item in enumerate(entries):
            # The code cannot be unified as format is different
            dtStart = QTableWidgetItem(item[0].strftime('%a %d %b %Y, %H:%M'))
            comment.setFlags(~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(i, 3, comment)