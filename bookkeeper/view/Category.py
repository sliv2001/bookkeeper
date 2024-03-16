from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox, QInputDialog, QTreeWidgetItem

from bookkeeper.view.Ui_Category import Ui_CategoryDialog
from bookkeeper.presenter.presenter import Presenter

class CategoryDialog(QDialog):

    presenter: Presenter
    topLevels: list
    dictOfAll: dict
    
    def displayCategories(self, parentWidget : QTreeWidgetItem = None):
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
        super(CategoryDialog, self).__init__()
        if presenter == None:
            self.presenter = parent.presenter
        else:
            self.presenter = presenter
        self.ui = Ui_CategoryDialog()
        self.ui.setupUi(self)
        self.presenter.updated.connect(self.updateTreeWidget)
        self.updateTreeWidget()
        

    @Slot()
    def on_pushButton_clicked(self):
        newCat, res = QInputDialog.getText(self, 'New category', 'Name new category: ')
        if res:
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
        self.presenter.commitCategories()
        return super().accept()

    @Slot()
    def reject(self) -> None:
        self.presenter.cancelCategories()
        return super().reject()

    @Slot()
    def updateTreeWidget(self) -> None:
        self.ui.treeWidget.clear()
        self.topLevels, self.dictOfAll = self.presenter.getCategoriesHierarchy()
        self.displayCategories()