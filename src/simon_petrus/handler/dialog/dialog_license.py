"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

from ui import dialog_license


class DialogLicense(QtWidgets.QDialog, dialog_license.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogLicense, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

    @pyqtSlot()
    def on_btn_close_clicked(self):
        self.close()
