# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/screen_loading_animation.ui'
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
        MainWindow.resize(528, 281)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 511, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 511, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.main_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.main_progress.setGeometry(QtCore.QRect(10, 200, 511, 23))
        self.main_progress.setProperty("value", 0)
        self.main_progress.setObjectName("main_progress")
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(10, 250, 511, 16))
        self.label_status.setObjectName("label_status")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 230, 511, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_gif = QtWidgets.QLabel(self.centralwidget)
        self.label_gif.setGeometry(QtCore.QRect(10, 70, 501, 121))
        self.label_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gif.setObjectName("label_gif")
        MainWindow.setCentralWidget(self.centralwidget)
        self.action_gen_cred = QtWidgets.QAction(MainWindow)
        self.action_gen_cred.setObjectName("action_gen_cred")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Menunggu ..."))
        self.label.setText(_translate("MainWindow", "Operasi Sedang Berjalan ..."))
        self.label_2.setText(_translate("MainWindow", "Menunggu memang tidak enak. Tetapi pernahkah Anda digantungin?"))
        self.label_status.setText(_translate("MainWindow", "-"))
        self.label_4.setText(_translate("MainWindow", "STATUS:"))
        self.label_gif.setText(_translate("MainWindow", "-"))
        self.action_gen_cred.setText(_translate("MainWindow", "Generate Secure Credential ..."))
        self.action_exit.setText(_translate("MainWindow", "Exit App"))
