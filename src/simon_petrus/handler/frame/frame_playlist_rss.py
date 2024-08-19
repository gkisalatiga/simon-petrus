"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
import os

from handler.dialog.dialog_banner import DialogBanner
from handler.dialog.dialog_poster import DialogPoster
from lib.mimetypes import MimeTypes
from ui import frame_playlist_rss


class FramePlaylistRSS(QtWidgets.QFrame, frame_playlist_rss.Ui_FrameRSS):
    def __init__(self, *args, obj=None, **kwargs):
        super(FramePlaylistRSS, self).__init__(*args, **kwargs)
        self.parent_button_box = None
        self.setupUi(self)
        self.b = DialogBanner(self)
        self.p = DialogPoster(self)

        # Validate on user input.
        self.field_title.textChanged.connect(self.validate_fields)
        self.field_key.textChanged.connect(self.validate_fields)

    def set_parent_button_box(self, parent_button_box: QtWidgets.QDialogButtonBox):
        self.parent_button_box = parent_button_box

    def validate_fields(self):
        parent_button_box = self.parent_button_box
        if parent_button_box is None:
            return

        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        rss_key = self.findChild(QtWidgets.QLineEdit, 'field_key').text().strip()

        if title == '' or rss_key == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan semua input!')
            parent_button_box.buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            parent_button_box.buttons()[0].setEnabled(True)
