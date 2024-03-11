from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox
from PySide6.QtGui import QAction

from bookkeeper.view.Ui_Budget import Ui_BudgetWindow

class BudgetView(QDialog):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(BudgetView, self).__init__()
        self.ui = Ui_BudgetWindow()
        self.ui.setupUi(self)
