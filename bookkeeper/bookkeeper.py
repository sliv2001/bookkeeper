"""
The file is the entry point of the project.
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, Qt, Slot, QMetaObject
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtGui import QAction

# TODO Remove generated ones
from bookkeeper.view.MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# TODO document every function
