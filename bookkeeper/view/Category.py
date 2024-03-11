from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QInputDialog, QTreeWidgetItem

from bookkeeper.view.Ui_Category import Ui_CategoryDialog
from bookkeeper.presenter.presenter import Presenter

class CategoryDialog(QDialog):

    presenter: Presenter

    def __init__(self, presenter: Presenter = None, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(CategoryDialog, self).__init__()
        if presenter == None:
            self.presenter = parent.presenter
        else:
            self.presenter = presenter
        self.ui = Ui_CategoryDialog()
        self.ui.setupUi(self)
        

    @Slot()
    def on_pushButton_clicked(self):
        item, res = QInputDialog.getText(self, 'Add category', 'New category: ')
        newItem = QTreeWidgetItem(self.ui.treeWidget.)

    @Slot()
    def accept(self) -> None:
        for i in self.ui.treeWidget.columnCount():
            for j in self.ui.treeWidget.columnAt():
        # for i in range(self.ui.listWidget.count()):
                self.presenter.addCategory(self.ui.treeWidget.itemAt(i, j).text())
        return super().accept()

    @Slot()
    def reject(self) -> None:
        return super().reject()