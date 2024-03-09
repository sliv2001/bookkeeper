import sys
from PySide6.QtWidgets import QApplication
from bookkeeper.view.MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    # Following variable must be assigned for interface to be shown
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# TODO document every function
