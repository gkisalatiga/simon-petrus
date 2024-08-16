"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets

from ui import dialog_agenda


class DialogAgenda(QtWidgets.QDialog, dialog_agenda.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogAgenda, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Input fields validation.
        self.field_name.textChanged.connect(self.validate_fields)
        self.field_place.textChanged.connect(self.validate_fields)
        self.field_representative.textChanged.connect(self.validate_fields)

    def validate_fields(self):
        name = self.findChild(QtWidgets.QLineEdit, 'field_name').text().strip()
        place = self.findChild(QtWidgets.QLineEdit, 'field_place').text().strip()
        representative = self.findChild(QtWidgets.QLineEdit, 'field_representative').text().strip()

        if name == '' or place == '' or representative == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan semua masukan!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(True)
