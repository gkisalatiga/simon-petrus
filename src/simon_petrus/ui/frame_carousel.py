# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/frame_carousel.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(580, 507)
        self.btn_save = QtWidgets.QPushButton(Frame)
        self.btn_save.setGeometry(QtCore.QRect(30, 450, 101, 31))
        self.btn_save.setObjectName("btn_save")
        self.day_selector = QtWidgets.QTabWidget(Frame)
        self.day_selector.setGeometry(QtCore.QRect(20, 260, 541, 181))
        self.day_selector.setObjectName("day_selector")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_yt_title = QtWidgets.QLabel(self.tab)
        self.label_yt_title.setGeometry(QtCore.QRect(10, 80, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_yt_title.setFont(font)
        self.label_yt_title.setObjectName("label_yt_title")
        self.label_yt_val = QtWidgets.QLabel(self.tab)
        self.label_yt_val.setGeometry(QtCore.QRect(200, 80, 321, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_yt_val.setFont(font)
        self.label_yt_val.setObjectName("label_yt_val")
        self.label_url_val = QtWidgets.QLabel(self.tab)
        self.label_url_val.setGeometry(QtCore.QRect(200, 100, 321, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_url_val.setFont(font)
        self.label_url_val.setObjectName("label_url_val")
        self.label_name = QtWidgets.QLabel(self.tab)
        self.label_name.setGeometry(QtCore.QRect(200, 20, 321, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_url_title = QtWidgets.QLabel(self.tab)
        self.label_url_title.setGeometry(QtCore.QRect(10, 100, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_url_title.setFont(font)
        self.label_url_title.setObjectName("label_url_title")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_type = QtWidgets.QLabel(self.tab)
        self.label_type.setGeometry(QtCore.QRect(200, 40, 321, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 20, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_date = QtWidgets.QLabel(self.tab)
        self.label_date.setGeometry(QtCore.QRect(200, 60, 321, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_date.setFont(font)
        self.label_date.setObjectName("label_date")
        self.label_poster = QtWidgets.QLabel(self.tab)
        self.label_poster.setGeometry(QtCore.QRect(10, 120, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_poster.setFont(font)
        self.label_poster.setObjectName("label_poster")
        self.btn_poster = QtWidgets.QPushButton(self.tab)
        self.btn_poster.setGeometry(QtCore.QRect(200, 120, 161, 24))
        self.btn_poster.setObjectName("btn_poster")
        self.day_selector.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.thumbnail_viewer = QtWidgets.QLabel(self.tab_2)
        self.thumbnail_viewer.setGeometry(QtCore.QRect(130, 0, 271, 151))
        self.thumbnail_viewer.setScaledContents(True)
        self.thumbnail_viewer.setObjectName("thumbnail_viewer")
        self.day_selector.addTab(self.tab_2, "")
        self.btn_delete = QtWidgets.QPushButton(Frame)
        self.btn_delete.setGeometry(QtCore.QRect(530, 220, 31, 31))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_add = QtWidgets.QPushButton(Frame)
        self.btn_add.setGeometry(QtCore.QRect(530, 60, 31, 31))
        self.btn_add.setObjectName("btn_add")
        self.btn_move_up = QtWidgets.QPushButton(Frame)
        self.btn_move_up.setEnabled(True)
        self.btn_move_up.setGeometry(QtCore.QRect(530, 100, 31, 31))
        self.btn_move_up.setObjectName("btn_move_up")
        self.btn_edit = QtWidgets.QPushButton(Frame)
        self.btn_edit.setGeometry(QtCore.QRect(530, 180, 31, 31))
        self.btn_edit.setObjectName("btn_edit")
        self.list_carousel = QtWidgets.QListWidget(Frame)
        self.list_carousel.setGeometry(QtCore.QRect(20, 60, 501, 191))
        self.list_carousel.setObjectName("list_carousel")
        self.btn_move_down = QtWidgets.QPushButton(Frame)
        self.btn_move_down.setEnabled(True)
        self.btn_move_down.setGeometry(QtCore.QRect(530, 140, 31, 31))
        self.btn_move_down.setObjectName("btn_move_down")
        self.app_title = QtWidgets.QLabel(Frame)
        self.app_title.setGeometry(QtCore.QRect(20, 10, 511, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.app_title.setObjectName("app_title")

        self.retranslateUi(Frame)
        self.day_selector.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.btn_save.setText(_translate("Frame", "✅    SIMPAN"))
        self.label_yt_title.setText(_translate("Frame", "Tautan YouTube"))
        self.label_yt_val.setText(_translate("Frame", "-"))
        self.label_url_val.setText(_translate("Frame", "-"))
        self.label_name.setText(_translate("Frame", "-"))
        self.label_3.setText(_translate("Frame", "Tanggal Pembuatan"))
        self.label_url_title.setText(_translate("Frame", "Tautan Artikel"))
        self.label_2.setText(_translate("Frame", "Jenis Pos"))
        self.label_type.setText(_translate("Frame", "-"))
        self.label.setText(_translate("Frame", "Judul "))
        self.label_date.setText(_translate("Frame", "-"))
        self.label_poster.setText(_translate("Frame", "Media Poster"))
        self.btn_poster.setText(_translate("Frame", "Tampilkan Poster ..."))
        self.day_selector.setTabText(self.day_selector.indexOf(self.tab), _translate("Frame", "Informasi Dasar"))
        self.thumbnail_viewer.setText(_translate("Frame", "-"))
        self.day_selector.setTabText(self.day_selector.indexOf(self.tab_2), _translate("Frame", "Thumbnail"))
        self.btn_delete.setToolTip(_translate("Frame", "Hapus formulir"))
        self.btn_delete.setText(_translate("Frame", "🗑"))
        self.btn_add.setToolTip(_translate("Frame", "Tambah formulir baru"))
        self.btn_add.setText(_translate("Frame", "➕"))
        self.btn_move_up.setToolTip(_translate("Frame", "Pindah posisi formulir ke atas"))
        self.btn_move_up.setText(_translate("Frame", "⏫"))
        self.btn_edit.setToolTip(_translate("Frame", "Ubah formulir terpilih"))
        self.btn_edit.setText(_translate("Frame", "🖉"))
        self.btn_move_down.setToolTip(_translate("Frame", "Pindah posisi formulir ke bawah"))
        self.btn_move_down.setText(_translate("Frame", "⏬"))
        self.app_title.setText(_translate("Frame", "Komedi Putar GKI Salatiga+"))
