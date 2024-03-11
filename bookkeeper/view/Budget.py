from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox
from PySide6.QtGui import QAction

from bookkeeper.view.Ui_Budget import Ui_BudgetWindow
from bookkeeper.presenter.presenter import Presenter

class BudgetView(QDialog):

    presenter: Presenter

    def __init__(self, presenter: Presenter = None, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(BudgetView, self).__init__()
        if presenter == None:
            self.presenter = self.parent().presenter
        else:
            self.presenter = presenter
        self.ui = Ui_BudgetWindow()
        self.ui.setupUi(self)

    @Slot()
    def accept(self) -> None:
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')
        return super().accept()

    @Slot()
    def reject(self) -> None:
        return super().reject()
