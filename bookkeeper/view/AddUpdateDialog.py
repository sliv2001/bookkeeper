from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget

from bookkeeper.view.Ui_AddUpdateDialog import Ui_AddUpdateDialog

class AddUpdateDialog(QDialog):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(AddUpdateDialog, self).__init__()
        self.ui = Ui_AddUpdateDialog()
        self.ui.setupUi(self)
