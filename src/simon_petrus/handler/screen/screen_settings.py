"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

import global_schema
from ui import screen_settings


class ScreenSettings(QtWidgets.QMainWindow, screen_settings.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenSettings, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Displaying the appropriate settings value in each field.
        self.chk_autosync.setChecked(True if global_schema.prefs.settings['autosync_on_launch'] == 1 else False)
        self.chk_gdrive_fetch_all.setChecked(True if global_schema.prefs.settings['gdrive_fetch_all_photos'] == 1 else False)

    @pyqtSlot()
    def on_btn_apply_clicked(self):
        # Saving the settings value.
        global_schema.prefs.settings['autosync_on_launch'] = 1 if self.chk_autosync.isChecked() is True else 0
        global_schema.prefs.settings['gdrive_fetch_all_photos'] = 1 if self.chk_gdrive_fetch_all.isChecked() is True else 0

        # Writing config into file.
        global_schema.prefs.save_config()

        # Notify the user that the settings have been saved.
        QtWidgets.QMessageBox.information(
            self, 'Berhasil menyimpan pengaturan!',
            'Pengaturan berhasil disimpan! Jendela pengaturan akan tertutup setelah ini.',
            QtWidgets.QMessageBox.Ok
        )

        # Finally, close this settings modal.
        self.close()

    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        self.close()
