import pytest
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtTest import QTest
from bookkeeper.view.MainWindow import MainWindow
from bookkeeper.presenter.presenter import Presenter

@pytest.fixture(scope="session")
def app():
    """
    Fixture to create a single QApplication instance for the entire test session.
    """
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    yield application
    application.quit()

@pytest.fixture
def main_window(app):
    """
    Fixture to create a MainWindow instance for testing.
    """
    window = MainWindow()
    window.show()
    return window

def test_initial_state(main_window):
    """
    Test initial state of the MainWindow UI components.
    """
    assert main_window.ui.tableWidget.rowCount() == 0
    assert main_window.ui.tableWidget.columnCount() == 4
    assert main_window.ui.summary.text() == 'Итого: 0₽ за последние 365 дней'

def test_update_main_view(main_window):
    """
    Test updating the main view of MainWindow.
    """
    # Simulate updating main view
    main_window.presenter.addCategory('category')
    main_window.presenter.commitCategories()
    main_window.presenter.addExpense('category', 100, datetime.now(), "comment")
    main_window.updateMainView()
    # Check if table widget is updated
    assert main_window.ui.tableWidget.rowCount() > 0
    assert main_window.ui.summary.text() != ''

