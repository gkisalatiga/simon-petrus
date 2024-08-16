"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

import global_schema
from ui import frame_renungan


class FrameRenungan(QtWidgets.QFrame, frame_renungan.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameRenungan, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Pre-fill the input fields with the data already present in the JSON schema.
        self.field_kiddy.setText(global_schema.app_db.db['ykb'][0]['url'])
        self.field_teens.setText(global_schema.app_db.db['ykb'][1]['url'])
        self.field_youth.setText(global_schema.app_db.db['ykb'][2]['url'])
        self.field_wasiat.setText(global_schema.app_db.db['ykb'][3]['url'])
        self.field_lansia.setText(global_schema.app_db.db['ykb'][4]['url'])

    @pyqtSlot()
    def on_btn_save_clicked(self):
        global_schema.app_db.db['ykb'][0]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_kiddy').text()
        global_schema.app_db.db['ykb'][1]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_teens').text()
        global_schema.app_db.db['ykb'][2]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_youth').text()
        global_schema.app_db.db['ykb'][3]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_wasiat').text()
        global_schema.app_db.db['ykb'][4]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_lansia').text()

        # Save to local file.
        global_schema.app_db.save_local('ykb')

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )
