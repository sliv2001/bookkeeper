import datetime

from PySide6.QtCore import Qt, Slot, QDateTime
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QDialogButtonBox

from bookkeeper.view.Ui_AddUpdateDialog import Ui_AddUpdateDialog
from bookkeeper.presenter.presenter import Presenter
from bookkeeper.view.Category import CategoryDialog

class AddUpdateDialog(QDialog):
    """
    Dialog for adding or updating expense entries.

    Args:
        presenter (Presenter, optional): Presenter object. Defaults to None.
        parent (QWidget | None, optional): Parent widget. Defaults to ... (None).
        flags (Qt.WindowType, optional): Window flags. Defaults to Qt.WindowType.
    """

    presenter: Presenter

    cats: list

    def __init__(self, presenter: Presenter = None, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        """
        Initializes the AddUpdateDialog.

        Args:
            presenter (Presenter, optional): Presenter object. Defaults to None.
            parent (QWidget | None, optional): Parent widget. Defaults to ... (None).
            flags (Qt.WindowType, optional): Window flags. Defaults to Qt.WindowType.
        """
        super(AddUpdateDialog, self).__init__()
        if presenter == None:
            self.presenter = parent.presenter
        else:
            self.presenter = presenter
        self.ui = Ui_AddUpdateDialog()
        self.ui.setupUi(self)
        self.updateAll()
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.presenter.updatedCategory.connect(self.updateAll)
        self.presenter.updatedExpense.connect(self.updateAll)

    def updateOkButton(self):
        """
        Update the state of the OK button based on input validity.
        """
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(self.ui.spinBox.value() > 0 and self.ui.comboBox.currentIndex() > -1)
    
    @Slot()
    def on_spinBox_textChanged(self):
        """
        Slot handling the change in spin box text.
        """
        self.updateOkButton()

    @Slot()
    def on_comboBox_currentIndexChanged(self):
        """
        Slot handling the change in combo box selection.
        """
        self.updateOkButton()

    @Slot()
    def on_pushButton_clicked(self):
        """
        Slot handling the click event of the push button.
        """
        self.categoryView = CategoryDialog(parent=self)
        self.categoryView.show()

    @Slot()
    def accept(self) -> None:
        # TODO add removeExpense to presenter

        """
        Slot handling the acceptance of the dialog.
        """
        category = self.ui.comboBox.itemText(self.ui.comboBox.currentIndex())
        value = int(self.ui.spinBox.text())
        dt = self.ui.dateTimeEdit.dateTime().toPython()
        comment = self.ui.plainTextEdit.toPlainText()
        self.presenter.addExpense(category, value, dt, comment)
        return super().accept()

    @Slot()
    def reject(self) -> None:
        """
        Slot handling the rejection of the dialog.
        """
        return super().reject()
        # TODO add removeExpense to presenter

    @Slot()
    def updateAll(self) -> None:
        """
        Slot to update all elements in the dialog.
        """
        self.cats = self.presenter.getAllCategories()
        self.ui.comboBox.setEnabled(len(self.cats) > 0)
        self.ui.comboBox.clear()
        self.ui.comboBox.insertItems(0, self.cats)
        self.updateOkButton()
