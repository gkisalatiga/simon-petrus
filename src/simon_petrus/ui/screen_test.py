# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/screen_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(594, 339)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.app_title = QtWidgets.QLabel(self.centralwidget)
        self.app_title.setGeometry(QtCore.QRect(20, 20, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.app_title.setObjectName("app_title")
        self.label_test = QtWidgets.QLabel(self.centralwidget)
        self.label_test.setGeometry(QtCore.QRect(20, 70, 281, 241))
        self.label_test.setScaledContents(True)
        self.label_test.setObjectName("label_test")
        MainWindow.setCentralWidget(self.centralwidget)
        self.action_gen_cred = QtWidgets.QAction(MainWindow)
        self.action_gen_cred.setObjectName("action_gen_cred")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "[DEBUG] Test Screen - Simon Petrus"))
        self.app_title.setText(_translate("MainWindow", "[DEBUG] This is the test screen."))
        self.label_test.setText(_translate("MainWindow", "-"))
        self.action_gen_cred.setText(_translate("MainWindow", "Generate Secure Credential ..."))
        self.action_exit.setText(_translate("MainWindow", "Exit App"))
