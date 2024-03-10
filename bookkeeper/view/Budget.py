from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QMessageBox
from PySide6.QtGui import QAction

from bookkeeper.view.Ui_Budget import Ui_BudgetWindow

class Budget(QMainWindow):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(Budget, self).__init__()
        self.ui = Ui_BudgetWindow()
        self.ui.setupUi(self)
