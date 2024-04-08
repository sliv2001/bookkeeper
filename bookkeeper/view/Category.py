from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QInputDialog, QTreeWidgetItem

from bookkeeper.view.Ui_Category import Ui_CategoryDialog
from bookkeeper.presenter.presenter import Presenter

class CategoryDialog(QDialog):
    """
    Dialog for managing categories.

    Args:
        presenter (Presenter, optional): Presenter object. Defaults to None.
        parent (QWidget | None, optional): Parent widget. Defaults to ... (None).
        flags (Qt.WindowType, optional): Window flags. Defaults to Qt.WindowType.
    """

    presenter: Presenter
    topLevels: list[str]
    dictOfAll: dict[str, list[str]]

    def displayCategories(self, parentWidget : QTreeWidgetItem = None):
        """
        Display categories in the tree widget.

        Args:
            parentWidget (QTreeWidgetItem, optional): Parent widget. Defaults to None.
        """
        if parentWidget == None:
            childrenList = self.topLevels
        else:
            childrenList = self.dictOfAll[parentWidget.text(0)]
            if childrenList==[]:
                return
        for item in childrenList:
            if parentWidget==None:
                treeItem = QTreeWidgetItem(self.ui.treeWidget)
            else:
                treeItem = QTreeWidgetItem(parentWidget)
            treeItem.setText(0, item)
            self.displayCategories(treeItem)

    def __init__(self, presenter: Presenter = None, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        """
        Initializes the CategoryDialog.

        Args:
            presenter (Presenter, optional): Presenter object. Defaults to None.
            parent (QWidget | None, optional): Parent widget. Defaults to ... (None).
            flags (Qt.WindowType, optional): Window flags. Defaults to Qt.WindowType.
        """
        super(CategoryDialog, self).__init__()
        if presenter == None:
            self.presenter = parent.presenter
        else:
            self.presenter = presenter
        self.ui = Ui_CategoryDialog()
        self.ui.setupUi(self)
        self.presenter.updatedCategory.connect(self.updateAll)
        self.updateAll()


    @Slot()
    def on_pushButton_clicked(self):
        """
        Slot handling the click event of the push button.
        """
        newCat, res = QInputDialog.getText(self, 'New category', 'Name new category: ')
        if res and len(newCat) > 0:
            if len(self.dictOfAll.keys())>0:
                parentCat, res = QInputDialog.getItem(self, 'Parent category', 'Choose parent category', list(self.dictOfAll.keys()) + ['None'])
                if res:
                    if parentCat=='None':
                        self.presenter.addCategory(newCat)
                    else:
                        self.presenter.addCategory(newCat, parentCat)
            else:
                self.presenter.addCategory(newCat)

    @Slot()
    def accept(self) -> None:
        """
        Slot handling the acceptance of the dialog.
        """
        self.presenter.commitCategories()
        return super().accept()

    @Slot()
    def reject(self) -> None:
        """
        Slot handling the rejection of the dialog.
        """
        self.presenter.cancelCategories()
        return super().reject()

    @Slot()
    def updateAll(self) -> None:
        """
        Update the categories in the dialog.
        """
        self.ui.treeWidget.clear()
        self.topLevels, self.dictOfAll = self.presenter.getCategoriesHierarchy()
        self.displayCategories()

        # TODO complete deletion, renaming, updating categories