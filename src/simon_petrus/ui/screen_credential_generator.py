# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/screen_credential_generator.ui'
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
        MainWindow.resize(830, 467)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.app_title = QtWidgets.QLabel(self.centralwidget)
        self.app_title.setGeometry(QtCore.QRect(10, 10, 591, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.app_title.setObjectName("app_title")
        self.app_subtitle = QtWidgets.QLabel(self.centralwidget)
        self.app_subtitle.setGeometry(QtCore.QRect(10, 40, 681, 21))
        self.app_subtitle.setObjectName("app_subtitle")
        self.btn_json_oauth_drive = QtWidgets.QPushButton(self.centralwidget)
        self.btn_json_oauth_drive.setGeometry(QtCore.QRect(190, 90, 111, 24))
        self.btn_json_oauth_drive.setObjectName("btn_json_oauth_drive")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 90, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.txt_cred_loc = QtWidgets.QLabel(self.centralwidget)
        self.txt_cred_loc.setGeometry(QtCore.QRect(310, 90, 491, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.txt_cred_loc.setFont(font)
        self.txt_cred_loc.setObjectName("txt_cred_loc")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 160, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.field_api_yt = QtWidgets.QLineEdit(self.centralwidget)
        self.field_api_yt.setGeometry(QtCore.QRect(190, 160, 611, 24))
        self.field_api_yt.setText("")
        self.field_api_yt.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.field_api_yt.setObjectName("field_api_yt")
        self.field_api_wp_user = QtWidgets.QLineEdit(self.centralwidget)
        self.field_api_wp_user.setGeometry(QtCore.QRect(190, 190, 611, 24))
        self.field_api_wp_user.setText("")
        self.field_api_wp_user.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.field_api_wp_user.setObjectName("field_api_wp_user")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 190, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.field_api_gh = QtWidgets.QLineEdit(self.centralwidget)
        self.field_api_gh.setGeometry(QtCore.QRect(190, 250, 611, 24))
        self.field_api_gh.setText("")
        self.field_api_gh.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.field_api_gh.setObjectName("field_api_gh")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 250, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.btn_gen = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen.setGeometry(QtCore.QRect(190, 340, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_gen.setFont(font)
        self.btn_gen.setObjectName("btn_gen")
        self.field_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.field_pass.setGeometry(QtCore.QRect(190, 300, 611, 24))
        self.field_pass.setText("")
        self.field_pass.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.field_pass.setObjectName("field_pass")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 300, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.txt_cred_loc_2 = QtWidgets.QLabel(self.centralwidget)
        self.txt_cred_loc_2.setGeometry(QtCore.QRect(190, 120, 611, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(False)
        self.txt_cred_loc_2.setFont(font)
        self.txt_cred_loc_2.setObjectName("txt_cred_loc_2")
        self.field_api_wp_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.field_api_wp_pass.setGeometry(QtCore.QRect(190, 220, 611, 24))
        self.field_api_wp_pass.setText("")
        self.field_api_wp_pass.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.field_api_wp_pass.setObjectName("field_api_wp_pass")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 220, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 830, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.btn_json_oauth_drive, self.field_api_yt)
        MainWindow.setTabOrder(self.field_api_yt, self.field_api_wp_user)
        MainWindow.setTabOrder(self.field_api_wp_user, self.field_api_wp_pass)
        MainWindow.setTabOrder(self.field_api_wp_pass, self.field_api_gh)
        MainWindow.setTabOrder(self.field_api_gh, self.field_pass)
        MainWindow.setTabOrder(self.field_pass, self.btn_gen)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simon Petrus - Credential Generator"))
        self.app_title.setText(_translate("MainWindow", "Simon Petrus - Credential Generator"))
        self.app_subtitle.setText(_translate("MainWindow", "Converts a list of API keys and IAM JSON file into an encrypted JSON file that can be parsed by Simon Petrus"))
        self.btn_json_oauth_drive.setText(_translate("MainWindow", "Select File ..."))
        self.label.setText(_translate("MainWindow", "Service Account JSON Key"))
        self.txt_cred_loc.setText(_translate("MainWindow", "No file is currently selected."))
        self.label_2.setText(_translate("MainWindow", "YouTube API V3 Key"))
        self.label_3.setText(_translate("MainWindow", "WordPress Username"))
        self.label_4.setText(_translate("MainWindow", "GitHub API Key"))
        self.btn_gen.setText(_translate("MainWindow", "GENERATE"))
        self.label_5.setText(_translate("MainWindow", "DECRYPTION PASSWORD"))
        self.txt_cred_loc_2.setText(_translate("MainWindow", "Must be a valid service account JSON key file generated in a Google Cloud Console project"))
        self.label_6.setText(_translate("MainWindow", "WordPress Password"))
