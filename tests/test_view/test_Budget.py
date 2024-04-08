import pytest

from PySide6.QtCore import Qt, QDateTime, QDate
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from pony import orm
from datetime import datetime, timedelta

from bookkeeper.view.Budget import BudgetView
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
def budget_view(app):
    """
    Fixture to create a BudgetView instance for testing.
    """
    view = BudgetView(Presenter())
    view.show()
    return view

def test_initial_state(budget_view):
    # Test initial state of UI components
    assert budget_view.ui.dateEdit.dateTime().date() == budget_view.ui.dateEdit_2.dateTime().date()
    assert budget_view.ui.spinBox.value() == 0
    assert budget_view.ui.tableWidget.rowCount() == 3

def test_add_budget(qtbot, budget_view):
    """
    Test adding a budget entry to the BudgetView.
    """
    initial_row_count = budget_view.ui.tableWidget.rowCount()
    test_start_date = QDate.currentDate()
    test_end_date = QDate.currentDate()
    budget_view.ui.spinBox.stepUp()
    qtbot.mouseClick(budget_view.ui.pushButton, Qt.LeftButton)
    QTest.qWaitForWindowExposed(budget_view)
    QTest.qWait(100)
    assert budget_view.ui.tableWidget.rowCount() == initial_row_count + 1
    assert budget_view.ui.tableWidget.item(3, 0).text() == test_start_date.toPython().strftime('%a %d %b %Y')
    assert budget_view.ui.tableWidget.item(3, 1).text() == test_end_date.toPython().strftime('%a %d %b %Y')

