from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget

from bookkeeper.view.Ui_Category import Ui_CategoryDialog

class CategoryDialog(QDialog):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(CategoryDialog, self).__init__()
        self.ui = Ui_CategoryDialog()
        self.ui.setupUi(self)
