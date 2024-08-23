"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets

from ui import dialog_static_folder


class DialogStaticFolder(QtWidgets.QDialog, dialog_static_folder.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogStaticFolder, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Input fields validation.
        self.field_title.textChanged.connect(self.validate_fields)
        self.field_url.textChanged.connect(self.validate_fields)

    def validate_fields(self):
        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()

        if title == '' or url == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan judul dan tautan gambar!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        elif not url.startswith('http') or not url.__contains__('://'):
            self.findChild(QtWidgets.QLabel, 'label_status').setText('URL Anda harus dimulai dengan "http://" atau "https://"!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(True)
