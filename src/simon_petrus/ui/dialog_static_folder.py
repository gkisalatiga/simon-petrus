# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/dialog_static_folder.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(519, 222)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setGeometry(QtCore.QRect(10, 180, 501, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.app_title = QtWidgets.QLabel(Dialog)
        self.app_title.setGeometry(QtCore.QRect(10, 10, 391, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.app_title.setObjectName("app_title")
        self.app_title_2 = QtWidgets.QLabel(Dialog)
        self.app_title_2.setGeometry(QtCore.QRect(10, 30, 491, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.app_title_2.setFont(font)
        self.app_title_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.app_title_2.setWordWrap(True)
        self.app_title_2.setObjectName("app_title_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 80, 131, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 131, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.field_title = QtWidgets.QLineEdit(Dialog)
        self.field_title.setGeometry(QtCore.QRect(162, 80, 341, 21))
        self.field_title.setObjectName("field_title")
        self.field_url = QtWidgets.QLineEdit(Dialog)
        self.field_url.setGeometry(QtCore.QRect(162, 110, 341, 21))
        self.field_url.setObjectName("field_url")
        self.label_status = QtWidgets.QLabel(Dialog)
        self.label_status.setGeometry(QtCore.QRect(160, 140, 341, 20))
        self.label_status.setObjectName("label_status")

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept) # type: ignore
        self.button_box.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tambah/Edit Folder Konten Profil"))
        self.app_title.setText(_translate("Dialog", "[Placeholder Title]"))
        self.app_title_2.setText(_translate("Dialog", "Masukkan judul dari folder konten profil GKI Salatiga beserta URL gambar utama dari folder yang akan ditampilkan pada halaman beranda GKI Salatiga+."))
        self.label.setText(_translate("Dialog", "Judul Folder"))
        self.label_2.setText(_translate("Dialog", "URL Gambar Folder"))
        self.field_title.setPlaceholderText(_translate("Dialog", "Profil GKI Salatiga, dsb."))
        self.field_url.setPlaceholderText(_translate("Dialog", "https://gkisalatiga.org/wp-content/gambar.png, dsb."))
        self.label_status.setText(_translate("Dialog", "-"))
