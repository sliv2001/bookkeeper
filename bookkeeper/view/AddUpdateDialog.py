from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox

from bookkeeper.view.Ui_AddUpdateDialog import Ui_AddUpdateDialog

class AddUpdateDialog(QDialog):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(AddUpdateDialog, self).__init__()
        self.ui = Ui_AddUpdateDialog()
        self.ui.setupUi(self)

    @Slot()
    def on_pushButton_clicked(self):
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')

    @Slot()
    def accept(self) -> None:
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')
        return super().accept()

    @Slot()
    def reject(self) -> None:
        return super().reject()
