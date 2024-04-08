# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Category.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHeaderView, QPushButton, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_CategoryDialog(object):
    def setupUi(self, CategoryDialog):
        if not CategoryDialog.objectName():
            CategoryDialog.setObjectName(u"CategoryDialog")
        CategoryDialog.resize(400, 300)
        CategoryDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(CategoryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeWidget = QTreeWidget(CategoryDialog)
        self.treeWidget.headerItem().setText(0, "")
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)

        self.pushButton = QPushButton(CategoryDialog)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.buttonBox = QDialogButtonBox(CategoryDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CategoryDialog)
        self.buttonBox.accepted.connect(CategoryDialog.accept)
        self.buttonBox.rejected.connect(CategoryDialog.reject)

        QMetaObject.connectSlotsByName(CategoryDialog)
    # setupUi

    def retranslateUi(self, CategoryDialog):
        CategoryDialog.setWindowTitle(QCoreApplication.translate("CategoryDialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("CategoryDialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
    # retranslateUi

