"""
This is main module of the application.
"""
import sys
from PySide6.QtWidgets import QApplication
from bookkeeper.view.MainWindow import MainWindow


def main():
    """
    Entry point of the application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
