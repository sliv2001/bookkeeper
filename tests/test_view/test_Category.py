import pytest

from PySide6.QtCore import Qt, QDateTime, QDate
from PySide6.QtWidgets import QApplication, QInputDialog, QDialogButtonBox
from PySide6.QtTest import QTest
from pony import orm
from datetime import datetime, timedelta

from bookkeeper.view.Category import CategoryDialog
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
def category_dialog(app):
    """
    Fixture to create a CategoryDialog instance for testing.
    """
    presenter = Presenter()
    # Remove all extras from previous testing
    presenter.delete_all()
    dialog = CategoryDialog(presenter)
    dialog.show()
    return dialog

def test_display_categories(qtbot, category_dialog):
    """
    Test displaying categories in the CategoryDialog.
    """
    # You may need to wait for the CategoryDialog to be exposed
    QTest.qWaitForWindowExposed(category_dialog)
    # Assert the initial state
    assert category_dialog.ui.treeWidget.topLevelItemCount() == 0
    # Call displayCategories method
    category_dialog.presenter.addCategory("Category 1")
    category_dialog.displayCategories()
    # Check if categories are displayed correctly
    assert category_dialog.ui.treeWidget.topLevelItemCount() > 0
