from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox

from bookkeeper.view.Ui_AddUpdateDialog import Ui_AddUpdateDialog
from bookkeeper.presenter.presenter import Presenter

class AddUpdateDialog(QDialog):

    presenter: Presenter

    def __init__(self, presenter: Presenter = None, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(AddUpdateDialog, self).__init__()
        if presenter == None:
            self.presenter = self.parent().presenter
        else:
            self.presenter = presenter
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
