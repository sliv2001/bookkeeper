import sys
import unittest
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QApplication, QDialogButtonBox
from bookkeeper.view.AddUpdateDialog import AddUpdateDialog
from bookkeeper.presenter.presenter import Presenter

class TestAddUpdateDialog(unittest.TestCase):
    """
    A test class for the AddUpdateDialog class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        """
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests have been run.
        """
        del cls.app

    def setUp(self):
        """
        Set up before each test.
        """
        self.presenter = Presenter()
        self.presenter.deleteALL()
        self.dialog = AddUpdateDialog(self.presenter)

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.dialog.close()
        del self.dialog
        del self.presenter

    def test_init(self):
        """
        Test the initialization of the dialog.
        """
        self.assertIsNotNone(self.dialog.presenter)
        self.assertIsNotNone(self.dialog.ui)
        self.assertIsNotNone(self.dialog.cats)

    def test_updateOkButton(self):
        """
        Test the updateOkButton method.
        """
        # Test when spinBox value and comboBox currentIndex are valid
        self.dialog.ui.spinBox.setValue(10)
        self.dialog.ui.comboBox.setCurrentIndex(0)
        self.dialog.updateOkButton()
        self.assertTrue(self.dialog.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).isEnabled())

        # Test when spinBox value is 0
        self.dialog.ui.spinBox.setValue(0)
        self.dialog.updateOkButton()
        self.assertFalse(self.dialog.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).isEnabled())

        # Test when comboBox currentIndex is -1
        self.dialog.ui.spinBox.setValue(10)
        self.dialog.ui.comboBox.setCurrentIndex(-1)
        self.dialog.updateOkButton()
        self.assertFalse(self.dialog.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).isEnabled())

    def test_updateAll(self):
        """
        Test the updateAll method.
        """
        # Assuming presenter has some categories
        self.presenter.addCategory("Category 1")
        self.presenter.addCategory("Category 2")
        self.dialog.updateAll()
        self.assertTrue(self.dialog.ui.comboBox.isEnabled())
        self.assertEqual(self.dialog.ui.comboBox.count(), 2)

    def test_accept(self):
        """
        Test the accept method.
        """
        # Assuming presenter has some categories
        self.presenter.addCategory("Category 1")
        self.presenter.addCategory("Category 2")
        self.presenter.commitCategories()

        # Setting values in UI
        self.dialog.ui.spinBox.setValue(100)
        self.dialog.ui.comboBox.setCurrentIndex(0)
        self.dialog.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.dialog.ui.plainTextEdit.setPlainText("Test comment")

        # Triggering accept
        self.dialog.accept()

        # Asserting if the expense is added
        self.assertEqual(len(self.presenter.getRecentExpenses(days=1)), 1)

    def test_reject(self):
        """
        Test the reject method.
        """
        self.dialog.reject()
        self.assertEqual(self.dialog.result(), 0)