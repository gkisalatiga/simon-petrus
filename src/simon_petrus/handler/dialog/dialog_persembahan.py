"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets

from ui import dialog_persembahan


class DialogPersembahan(QtWidgets.QDialog, dialog_persembahan.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogPersembahan, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Input fields validation.
        self.field_bank_abbr.textChanged.connect(self.validate_fields)
        self.field_bank_name.textChanged.connect(self.validate_fields)
        self.field_number.textChanged.connect(self.validate_fields)
        self.field_holder.textChanged.connect(self.validate_fields)

    def validate_fields(self):
        bank_abbr = self.findChild(QtWidgets.QLineEdit, 'field_bank_abbr').text().strip()
        bank_name = self.findChild(QtWidgets.QLineEdit, 'field_bank_name').text().strip()
        number = self.findChild(QtWidgets.QLineEdit, 'field_number').text().strip()
        holder = self.findChild(QtWidgets.QLineEdit, 'field_holder').text().strip()

        if bank_abbr == '' or bank_name == '' or number == '' or holder == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan semua masukan!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(True)
