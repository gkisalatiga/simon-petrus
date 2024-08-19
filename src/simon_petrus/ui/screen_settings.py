# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/screen_settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.btn_apply = QtWidgets.QPushButton(self.centralwidget)
        self.btn_apply.setGeometry(QtCore.QRect(350, 20, 111, 31))
        self.btn_apply.setObjectName("btn_apply")
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(470, 20, 111, 31))
        self.btn_cancel.setObjectName("btn_cancel")
        self.chk_autosync = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_autosync.setGeometry(QtCore.QRect(20, 80, 551, 22))
        self.chk_autosync.setChecked(True)
        self.chk_autosync.setObjectName("chk_autosync")
        self.chk_gdrive_fetch_all = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_gdrive_fetch_all.setGeometry(QtCore.QRect(20, 130, 551, 22))
        self.chk_gdrive_fetch_all.setChecked(False)
        self.chk_gdrive_fetch_all.setObjectName("chk_gdrive_fetch_all")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 150, 541, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.action_gen_cred = QtWidgets.QAction(MainWindow)
        self.action_gen_cred.setObjectName("action_gen_cred")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pengaturan Aplikasi - Simon Petrus"))
        self.label.setText(_translate("MainWindow", "Pengaturan Umum"))
        self.btn_apply.setText(_translate("MainWindow", "✅     SIMPAN"))
        self.btn_cancel.setText(_translate("MainWindow", "❌     BATALKAN"))
        self.chk_autosync.setText(_translate("MainWindow", "Otomatis sinkronisasi data pada saat aplikasi dijalankan"))
        self.chk_gdrive_fetch_all.setText(_translate("MainWindow", "Sinkronisasi semua foto Google Drive pada menu \"Galeri\" GKI Salatiga+"))
        self.label_2.setText(_translate("MainWindow", "Jika dimatikan, sinkronisasi folder pada galeri GKI Salatiga+\n"
"hanya akan mengambil 100 foto pertama dari folder Google Drive"))
        self.action_gen_cred.setText(_translate("MainWindow", "Generate Secure Credential ..."))
        self.action_exit.setText(_translate("MainWindow", "Exit App"))
