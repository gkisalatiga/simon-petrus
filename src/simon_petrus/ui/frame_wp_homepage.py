# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/frame_wp_homepage.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(580, 446)
        self.app_title = QtWidgets.QLabel(Frame)
        self.app_title.setGeometry(QtCore.QRect(20, 20, 511, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.app_title.setObjectName("app_title")
        self.txt_label2 = QtWidgets.QLabel(Frame)
        self.txt_label2.setGeometry(QtCore.QRect(20, 60, 551, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.txt_label2.setFont(font)
        self.txt_label2.setObjectName("txt_label2")
        self.checkBox = QtWidgets.QCheckBox(Frame)
        self.checkBox.setEnabled(False)
        self.checkBox.setGeometry(QtCore.QRect(200, 240, 341, 31))
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.label_8 = QtWidgets.QLabel(Frame)
        self.label_8.setGeometry(QtCore.QRect(20, 240, 171, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.checkBox_2 = QtWidgets.QCheckBox(Frame)
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setGeometry(QtCore.QRect(200, 270, 341, 31))
        self.checkBox_2.setCheckable(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.label_9 = QtWidgets.QLabel(Frame)
        self.label_9.setGeometry(QtCore.QRect(20, 270, 171, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Frame)
        self.label_10.setGeometry(QtCore.QRect(20, 150, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.field_yt_link = QtWidgets.QLineEdit(Frame)
        self.field_yt_link.setEnabled(False)
        self.field_yt_link.setGeometry(QtCore.QRect(200, 180, 361, 24))
        self.field_yt_link.setInputMask("")
        self.field_yt_link.setObjectName("field_yt_link")
        self.label_11 = QtWidgets.QLabel(Frame)
        self.label_11.setGeometry(QtCore.QRect(20, 300, 171, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.check_autodetect_ig = QtWidgets.QCheckBox(Frame)
        self.check_autodetect_ig.setEnabled(True)
        self.check_autodetect_ig.setGeometry(QtCore.QRect(200, 300, 341, 31))
        self.check_autodetect_ig.setCheckable(True)
        self.check_autodetect_ig.setChecked(True)
        self.check_autodetect_ig.setObjectName("check_autodetect_ig")
        self.txt_img_loc = QtWidgets.QLabel(Frame)
        self.txt_img_loc.setEnabled(False)
        self.txt_img_loc.setGeometry(QtCore.QRect(320, 340, 251, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.txt_img_loc.setFont(font)
        self.txt_img_loc.setObjectName("txt_img_loc")
        self.btn_img_select = QtWidgets.QPushButton(Frame)
        self.btn_img_select.setEnabled(False)
        self.btn_img_select.setGeometry(QtCore.QRect(200, 340, 111, 24))
        self.btn_img_select.setObjectName("btn_img_select")
        self.btn_execute = QtWidgets.QPushButton(Frame)
        self.btn_execute.setGeometry(QtCore.QRect(200, 380, 101, 31))
        self.btn_execute.setObjectName("btn_execute")
        self.label_status = QtWidgets.QLabel(Frame)
        self.label_status.setGeometry(QtCore.QRect(310, 380, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.label_status.setFont(font)
        self.label_status.setObjectName("label_status")
        self.check_autodetect_yt = QtWidgets.QCheckBox(Frame)
        self.check_autodetect_yt.setEnabled(True)
        self.check_autodetect_yt.setGeometry(QtCore.QRect(200, 150, 341, 21))
        self.check_autodetect_yt.setCheckable(True)
        self.check_autodetect_yt.setChecked(True)
        self.check_autodetect_yt.setObjectName("check_autodetect_yt")
        self.label_yt_helper = QtWidgets.QLabel(Frame)
        self.label_yt_helper.setEnabled(True)
        self.label_yt_helper.setGeometry(QtCore.QRect(200, 210, 361, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.label_yt_helper.setFont(font)
        self.label_yt_helper.setObjectName("label_yt_helper")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.app_title.setText(_translate("Frame", "Perbarui Laman Utama WordPress"))
        self.txt_label2.setText(_translate("Frame", "Fitur ini secara otomatis memperbarui halaman depan GKISalatiga.org\n"
"serta mengambil poster ibadah mingguan dari Instagram @gkisalatiga\n"
"secara programatis."))
        self.checkBox.setText(_translate("Frame", "Deteksi otomatis pos PDF warta jemaat terkini"))
        self.label_8.setText(_translate("Frame", "Warta Jemaat"))
        self.checkBox_2.setText(_translate("Frame", "Deteksi otomatis pos PDF tata ibadah terkini"))
        self.label_9.setText(_translate("Frame", "Tata Ibadah"))
        self.label_10.setText(_translate("Frame", "Live Streaming YouTube"))
        self.field_yt_link.setPlaceholderText(_translate("Frame", "Tautan YouTube live streaming ibadah"))
        self.label_11.setText(_translate("Frame", "Poster Ibadah"))
        self.check_autodetect_ig.setText(_translate("Frame", "Deteksi otomatis melalui pos Instagram"))
        self.txt_img_loc.setText(_translate("Frame", "Tidak ada berkas terpilih."))
        self.btn_img_select.setText(_translate("Frame", "Pilih Berkas ..."))
        self.btn_execute.setText(_translate("Frame", "🚀    PERBARUI"))
        self.label_status.setText(_translate("Frame", "-"))
        self.check_autodetect_yt.setToolTip(_translate("Frame", "Ambil data streaming YouTube terkini dari playlist \"Kebaktian Umum\" di YouTube GKI Salatiga"))
        self.check_autodetect_yt.setText(_translate("Frame", "Deteksi otomatis unggahan streaming YouTube terkini"))
        self.label_yt_helper.setText(_translate("Frame", "Tautan harus dimulai dengan \"https://www.youtube.com/watch?v=\""))