"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

import global_schema
from ui import frame_social_media


class FrameSocialMedia(QtWidgets.QFrame, frame_social_media.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameSocialMedia, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Pre-fill the input fields with the data already present in the JSON schema.
        self.field_email.setText(global_schema.app_db.db['url-profile']['email'])
        self.field_fb.setText(global_schema.app_db.db['url-profile']['fb'])
        self.field_ig.setText(global_schema.app_db.db['url-profile']['insta'])
        self.field_wa.setText(global_schema.app_db.db['url-profile']['whatsapp'])
        self.field_web.setText(global_schema.app_db.db['url-profile']['web'])
        self.field_yt.setText(global_schema.app_db.db['url-profile']['youtube'])

    @pyqtSlot()
    def on_btn_save_clicked(self):
        global_schema.app_db.db['url-profile']['email'] = self.findChild(QtWidgets.QLineEdit, 'field_email').text()
        global_schema.app_db.db['url-profile']['fb'] = self.findChild(QtWidgets.QLineEdit, 'field_fb').text()
        global_schema.app_db.db['url-profile']['insta'] = self.findChild(QtWidgets.QLineEdit, 'field_ig').text()
        global_schema.app_db.db['url-profile']['whatsapp'] = self.findChild(QtWidgets.QLineEdit, 'field_wa').text()
        global_schema.app_db.db['url-profile']['web'] = self.findChild(QtWidgets.QLineEdit, 'field_web').text()
        global_schema.app_db.db['url-profile']['youtube'] = self.findChild(QtWidgets.QLineEdit, 'field_yt').text()

        # Save to local file.
        global_schema.app_db.save_local('url-profile')

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )
