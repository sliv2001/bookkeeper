from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QDialogButtonBox

from bookkeeper.view.Ui_AddUpdateDialog import Ui_AddUpdateDialog
from bookkeeper.presenter.presenter import Presenter
from bookkeeper.view.Category import CategoryDialog

class AddUpdateDialog(QDialog):

    presenter: Presenter

    cats: list

    def __init__(self, presenter: Presenter = None, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(AddUpdateDialog, self).__init__()
        if presenter == None:
            self.presenter = parent.presenter
        else:
            self.presenter = presenter
        self.ui = Ui_AddUpdateDialog()
        self.ui.setupUi(self)
        self.updateAll()
        self.presenter.updatedCategory.connect(self.updateAll)

    @Slot()
    def on_pushButton_clicked(self):
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')

    @Slot()
    def on_lineEdit_textEdited(self):
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(len(self.ui.lineEdit.text()) > 0)

    @Slot()
    def on_pushButton_clicked(self):
        self.categoryView = CategoryDialog(parent=self)
        self.categoryView.show()

    @Slot()
    def accept(self) -> None:
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')
        return super().accept()

    @Slot()
    def reject(self) -> None:
        return super().reject()

    @Slot()
    def updateAll(self) -> None:
        self.cats = self.presenter.getAllCategories()
        self.ui.comboBox.setEnabled(len(self.cats)>0)
        self.ui.comboBox.clear()
        self.ui.comboBox.insertItems(0, self.cats)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(len(self.ui.lineEdit.text()) > 0)
