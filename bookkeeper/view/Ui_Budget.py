# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Budget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDateEdit, QDialog,
    QDialogButtonBox, QGridLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpinBox, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_BudgetWindow(object):
    def setupUi(self, BudgetWindow):
        if not BudgetWindow.objectName():
            BudgetWindow.setObjectName(u"BudgetWindow")
        BudgetWindow.resize(539, 499)
        BudgetWindow.setModal(True)
        self.verticalLayout = QVBoxLayout(BudgetWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableWidget = QTableWidget(BudgetWindow)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_3.addWidget(self.tableWidget)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.label_2 = QLabel(BudgetWindow)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.dateEdit = QDateEdit(BudgetWindow)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setCalendarPopup(True)

        self.gridLayout_3.addWidget(self.dateEdit, 0, 1, 1, 1)

        self.dateEdit_2 = QDateEdit(BudgetWindow)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setCalendarPopup(True)

        self.gridLayout_3.addWidget(self.dateEdit_2, 1, 1, 1, 1)

        self.label_4 = QLabel(BudgetWindow)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)

        self.spinBox = QSpinBox(BudgetWindow)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setSingleStep(100)

        self.gridLayout_3.addWidget(self.spinBox, 2, 1, 1, 1)

        self.label_3 = QLabel(BudgetWindow)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_5 = QLabel(BudgetWindow)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)

        self.pushButton = QPushButton(BudgetWindow)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_3.addWidget(self.pushButton, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.buttonBox = QDialogButtonBox(BudgetWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(BudgetWindow)
        self.buttonBox.accepted.connect(BudgetWindow.accept)
        self.buttonBox.rejected.connect(BudgetWindow.reject)

        QMetaObject.connectSlotsByName(BudgetWindow)
    # setupUi

    def retranslateUi(self, BudgetWindow):
        BudgetWindow.setWindowTitle(QCoreApplication.translate("BudgetWindow", u"Dialog", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("BudgetWindow", u"\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("BudgetWindow", u"\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("BudgetWindow", u"\u0417\u0430\u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u0440\u0430\u0441\u0445\u043e\u0434", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("BudgetWindow", u"\u0417\u0430\u043f\u0430\u0441", None));
        self.label_2.setText(QCoreApplication.translate("BudgetWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u0442\u0440\u0435\u043a\u0435\u0440:", None))
        self.label_4.setText(QCoreApplication.translate("BudgetWindow", u"\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f:", None))
        self.label_3.setText(QCoreApplication.translate("BudgetWindow", u"\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430:", None))
        self.label_5.setText(QCoreApplication.translate("BudgetWindow", u"\u041f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u043c\u044b\u0439 \u0440\u0430\u0441\u0445\u043e\u0434:", None))
        self.pushButton.setText(QCoreApplication.translate("BudgetWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
    # retranslateUi

