# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/frame_renungan.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(580, 376)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(20, 20, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.field_kiddy = QtWidgets.QLineEdit(Frame)
        self.field_kiddy.setGeometry(QtCore.QRect(170, 20, 301, 24))
        self.field_kiddy.setObjectName("field_kiddy")
        self.field_teens = QtWidgets.QLineEdit(Frame)
        self.field_teens.setGeometry(QtCore.QRect(170, 50, 301, 24))
        self.field_teens.setObjectName("field_teens")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.field_youth = QtWidgets.QLineEdit(Frame)
        self.field_youth.setGeometry(QtCore.QRect(170, 80, 301, 24))
        self.field_youth.setObjectName("field_youth")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.field_wasiat = QtWidgets.QLineEdit(Frame)
        self.field_wasiat.setGeometry(QtCore.QRect(170, 110, 301, 24))
        self.field_wasiat.setObjectName("field_wasiat")
        self.label_4 = QtWidgets.QLabel(Frame)
        self.label_4.setGeometry(QtCore.QRect(20, 110, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Frame)
        self.label_5.setGeometry(QtCore.QRect(20, 140, 141, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.field_lansia = QtWidgets.QLineEdit(Frame)
        self.field_lansia.setGeometry(QtCore.QRect(170, 140, 301, 24))
        self.field_lansia.setObjectName("field_lansia")
        self.btn_save = QtWidgets.QPushButton(Frame)
        self.btn_save.setGeometry(QtCore.QRect(170, 180, 101, 31))
        self.btn_save.setObjectName("btn_save")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label.setText(_translate("Frame", "Renungan Kiddy"))
        self.label_2.setText(_translate("Frame", "Teens for Christ"))
        self.label_3.setText(_translate("Frame", "Youth for Christ"))
        self.label_4.setText(_translate("Frame", "Renungan Wasiat"))
        self.label_5.setText(_translate("Frame", "Renungan Usia Indah"))
        self.btn_save.setText(_translate("Frame", "✅    SIMPAN"))
