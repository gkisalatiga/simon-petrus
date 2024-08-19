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
from ui import frame_playlist_regular


class FramePlaylistRegular(QtWidgets.QFrame, frame_playlist_regular.Ui_FrameRegular):
    def __init__(self, *args, obj=None, **kwargs):
        super(FramePlaylistRegular, self).__init__(*args, **kwargs)
        self.parent_button_box = None
        self.setupUi(self)
        self.b = DialogBanner(self)
        self.p = DialogPoster(self)

        # Validate on user input.
        self.field_title.textChanged.connect(self.validate_fields)
        self.field_url.textChanged.connect(self.validate_fields)

    def set_parent_button_box(self, parent_button_box: QtWidgets.QDialogButtonBox):
        self.parent_button_box = parent_button_box

    def validate_fields(self):
        parent_button_box = self.parent_button_box
        if parent_button_box is None:
            return

        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()

        if title == '' or url == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan semua input!')
            parent_button_box.buttons()[0].setEnabled(False)
        elif not url.startswith('http') or not url.__contains__('://') or not url.__contains__('list='):
            self.findChild(QtWidgets.QLabel, 'label_status').setText('URL Anda bukanlah URL daftar putar YouTube yang valid!')
            parent_button_box.buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            parent_button_box.buttons()[0].setEnabled(True)
