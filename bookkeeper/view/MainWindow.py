from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QMessageBox
from PySide6.QtGui import QAction

from bookkeeper.view.Ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @Slot()
    def on_actionAddOperation_triggered(self):
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')
        
    @Slot()
    def on_actionShowBudget_triggered(self):
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')
        
    @Slot()
    def on_actionAlterCats_triggered(self):
        QMessageBox.warning(self, 'Implementation Error', 'This feature is not implemented yet!')