# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddUpdateDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateTimeEdit,
    QDialog, QDialogButtonBox, QGridLayout, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_AddUpdateDialog(object):
    def setupUi(self, AddUpdateDialog):
        if not AddUpdateDialog.objectName():
            AddUpdateDialog.setObjectName(u"AddUpdateDialog")
        AddUpdateDialog.resize(553, 207)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddUpdateDialog.sizePolicy().hasHeightForWidth())
        AddUpdateDialog.setSizePolicy(sizePolicy)
        AddUpdateDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(AddUpdateDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_2 = QLabel(AddUpdateDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)

        self.pushButton = QPushButton(AddUpdateDialog)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_4.addWidget(self.pushButton, 2, 2, 1, 1)

        self.plainTextEdit = QPlainTextEdit(AddUpdateDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout_4.addWidget(self.plainTextEdit, 4, 1, 1, 1)

        self.comboBox = QComboBox(AddUpdateDialog)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_4.addWidget(self.comboBox, 2, 1, 1, 1)

        self.label = QLabel(AddUpdateDialog)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 1)

        self.label_4 = QLabel(AddUpdateDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_3 = QLabel(AddUpdateDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)

        self.dateTimeEdit = QDateTimeEdit(AddUpdateDialog)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setFocusPolicy(Qt.StrongFocus)
        self.dateTimeEdit.setCalendarPopup(True)

        self.gridLayout_4.addWidget(self.dateTimeEdit, 0, 1, 1, 1)

        self.spinBox = QSpinBox(AddUpdateDialog)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setSingleStep(100)

        self.gridLayout_4.addWidget(self.spinBox, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_4)

        self.buttonBox = QDialogButtonBox(AddUpdateDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.dateTimeEdit, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.plainTextEdit)

        self.retranslateUi(AddUpdateDialog)
        self.buttonBox.accepted.connect(AddUpdateDialog.accept)
        self.buttonBox.rejected.connect(AddUpdateDialog.reject)

        QMetaObject.connectSlotsByName(AddUpdateDialog)
    # setupUi

    def retranslateUi(self, AddUpdateDialog):
        AddUpdateDialog.setWindowTitle(QCoreApplication.translate("AddUpdateDialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("AddUpdateDialog", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
        self.pushButton.setText(QCoreApplication.translate("AddUpdateDialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.plainTextEdit.setPlainText("")
        self.label.setText(QCoreApplication.translate("AddUpdateDialog", u"\u0421\u0443\u043c\u043c\u0430", None))
        self.label_4.setText(QCoreApplication.translate("AddUpdateDialog", u"\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439", None))
        self.label_3.setText(QCoreApplication.translate("AddUpdateDialog", u"\u0414\u0430\u0442\u0430 \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f", None))
    # retranslateUi

