# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/frame_social_media.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(580, 376)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(20, 70, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.field_web = QtWidgets.QLineEdit(Frame)
        self.field_web.setGeometry(QtCore.QRect(140, 70, 331, 24))
        self.field_web.setObjectName("field_web")
        self.field_fb = QtWidgets.QLineEdit(Frame)
        self.field_fb.setGeometry(QtCore.QRect(140, 100, 331, 24))
        self.field_fb.setObjectName("field_fb")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.field_ig = QtWidgets.QLineEdit(Frame)
        self.field_ig.setGeometry(QtCore.QRect(140, 130, 331, 24))
        self.field_ig.setObjectName("field_ig")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.field_yt = QtWidgets.QLineEdit(Frame)
        self.field_yt.setGeometry(QtCore.QRect(140, 160, 331, 24))
        self.field_yt.setObjectName("field_yt")
        self.label_4 = QtWidgets.QLabel(Frame)
        self.label_4.setGeometry(QtCore.QRect(20, 160, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Frame)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.field_wa = QtWidgets.QLineEdit(Frame)
        self.field_wa.setGeometry(QtCore.QRect(140, 190, 331, 24))
        self.field_wa.setObjectName("field_wa")
        self.label_6 = QtWidgets.QLabel(Frame)
        self.label_6.setGeometry(QtCore.QRect(20, 220, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.field_email = QtWidgets.QLineEdit(Frame)
        self.field_email.setGeometry(QtCore.QRect(140, 220, 331, 24))
        self.field_email.setObjectName("field_email")
        self.btn_save = QtWidgets.QPushButton(Frame)
        self.btn_save.setGeometry(QtCore.QRect(140, 260, 101, 31))
        self.btn_save.setObjectName("btn_save")
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
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label.setText(_translate("Frame", "Situs Web"))
        self.label_2.setText(_translate("Frame", "Facebook"))
        self.label_3.setText(_translate("Frame", "Instagram"))
        self.label_4.setText(_translate("Frame", "YouTube"))
        self.label_5.setText(_translate("Frame", "WhatsApp"))
        self.label_6.setText(_translate("Frame", "E-Surat"))
        self.btn_save.setText(_translate("Frame", "✅    SIMPAN"))
        self.app_title.setText(_translate("Frame", "Media Sosial GKI Salatiga"))
