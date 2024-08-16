"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets

from ui import dialog_gallery


class DialogGallery(QtWidgets.QDialog, dialog_gallery.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogGallery, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Input fields validation.
        self.field_title.textChanged.connect(self.validate_fields)
        self.field_url.textChanged.connect(self.validate_fields)
        self.field_story.textChanged.connect(self.validate_fields)

    def validate_fields(self):
        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()
        story = self.findChild(QtWidgets.QPlainTextEdit, 'field_story').toPlainText().strip()

        if title == '' or url == '' or story == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan judul, tautan Google Drive, dan kisah!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        elif not url.startswith('https://drive.google.com/drive/folders'):
            self.findChild(QtWidgets.QLabel, 'label_status').setText('URL Anda harus dimulai dengan "https://drive.google.com/drive/folders"!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(True)
