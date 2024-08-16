"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets

from ui import dialog_banner


class DialogBanner(QtWidgets.QDialog, dialog_banner.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogBanner, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())
