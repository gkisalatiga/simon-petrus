# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/frame_default.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(580, 446)
        self.txt_cred_loc_2 = QtWidgets.QLabel(Frame)
        self.txt_cred_loc_2.setGeometry(QtCore.QRect(20, 20, 551, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.txt_cred_loc_2.setFont(font)
        self.txt_cred_loc_2.setObjectName("txt_cred_loc_2")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.txt_cred_loc_2.setText(_translate("Frame", "Selamat datang di Simon Petrus!"))
