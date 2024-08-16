"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

import global_schema
from handler.screen.screen_credential_generate import ScreenCredentialGenerate
from handler.screen.screen_main import ScreenMain
from lib.credentials import CredentialValidator
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from ui import screen_credential_decrypt


class ScreenCredentialDecrypt(QtWidgets.QMainWindow, screen_credential_decrypt.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenCredentialDecrypt, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # The temporary value of the selected credential location.
        self.cred_loc = ''

        # Whether there is a saved credential location.
        if global_schema.prefs.settings['remember_cred_loc'] == 1 and global_schema.prefs.settings['saved_cred_loc'] != '':
            self.cred_loc = global_schema.prefs.settings['saved_cred_loc']
            self.chk_save_cred_loc.setChecked(True)
            self.txt_cred_loc.setText(global_schema.prefs.settings['saved_cred_loc'])
            self.txt_cred_loc.setToolTip(global_schema.prefs.settings['saved_cred_loc'])

        # Log the in-app temporary OAUTH2.0 credential location.
        Lg('main.ScreenCredentialDecrypt.__init__', f'Saved OAUTH2.0 file path: {self.cred_loc}')

    @pyqtSlot()
    def on_action_gen_cred_triggered(self):
        ScreenCredentialGenerate(self).show()

    @pyqtSlot()
    def on_action_exit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_btn_cred_selector_clicked(self):
        ff = 'Encrypted JSON file (*.json.enc)'
        loc = QtWidgets.QFileDialog.getOpenFileName(self, 'Import admin credential file from ...', '', ff)[0]
        if not loc == '':
            self.cred_loc = loc
            self.txt_cred_loc.setText(self.cred_loc)
            self.txt_cred_loc.setToolTip(self.cred_loc)

    @pyqtSlot()
    def on_btn_decrypt_clicked(self):
        # Whether to save the credential location.
        if self.chk_save_cred_loc.isChecked() and self.cred_loc != '':
            global_schema.prefs.settings['remember_cred_loc'] = 1
            global_schema.prefs.settings['saved_cred_loc'] = self.txt_cred_loc.text()
        else:
            global_schema.prefs.settings['remember_cred_loc'] = 0
            global_schema.prefs.settings['saved_cred_loc'] = ''

        # Save the settings.
        global_schema.prefs.save_config()

        # Change the status.
        self.label_status.setText('Attempting to decrypt the credential data ...')
        QtCore.QCoreApplication.processEvents()

        # Validate the input credential file, and attempt to decrypt the input bytes.
        password_key = self.field_cred.text()
        validator = CredentialValidator(self.cred_loc)

        # Open the animation window and disable all elements in this window, to prevent user input.
        global_schema.anim.clear_and_show()
        global_schema.disable_widget(self)

        # Using multithreading to prevent GUI freezing [9]
        t = ThreadWithResult(target=validator.decrypt, args=(password_key,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                is_valid, decrypted_dict, message = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Closing the loading animation and re-enable the window.
        global_schema.enable_widget(self)
        global_schema.anim.hide()

        # Display whatever status message returned from the decryption to the user.
        msg_title = 'Decryption successful!' if is_valid else 'Failed to decrypt the credential data!'
        self.label_status.setText(msg_title)
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMessageBox.warning(
            self, msg_title, message,
            QtWidgets.QMessageBox.Ok
        )

        if is_valid:
            global_schema.app_db.populate_credentials(decrypted_dict)

            # Adjust the credentials of the assets manager.
            global_schema.app_assets.set_credentials(global_schema.app_db.credentials)

            # Preparing the JSON schema, ensuring that we have a valid data.
            global_schema.app_db.load_json_schema()

            # If we do not have a valid JSON schema, attempt to refresh from GitHub repo.
            if not global_schema.app_db.is_db_exist or not global_schema.app_db.is_db_valid or global_schema.prefs.settings['autosync_on_launch'] == 1:

                # Disable all elements in this window for a while, to prevent user input.
                global_schema.disable_widget(self)

                # Using multithreading to prevent GUI freezing [9]
                t = ThreadWithResult(target=global_schema.refresh_all_data, args=())
                t.start()
                while True:
                    if getattr(t, 'result', None):
                        # Obtaining the thread function's result
                        _ = t.result
                        t.join()

                        break
                    else:
                        # When this block is reached, it means the function has not returned any value
                        # While we wait for the thread response to be returned, let us prevent
                        # Qt5 GUI freezing by repeatedly executing the following line:
                        QtCore.QCoreApplication.processEvents()

                # Re-enable the window.
                global_schema.enable_widget(self)

            # Open the control panel (administrator dashboard).
            self.hide()
            # ScreenMain(self).show()
            global_schema.win_main = ScreenMain(self)
            global_schema.win_main.show()

    @pyqtSlot()
    def on_btn_exit_clicked(self):
        self.close()

    @pyqtSlot()
    def on_btn_show_pass_clicked(self):
        if self.field_cred.echoMode() == QtWidgets.QLineEdit.Password:
            self.field_cred.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.field_cred.setEchoMode(QtWidgets.QLineEdit.Password)
