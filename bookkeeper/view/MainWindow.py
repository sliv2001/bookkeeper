from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt, Slot, QMetaObject
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtGui import QAction

# TODO translate all to russian

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(800, 600)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setDockNestingEnabled(False)
        self.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
