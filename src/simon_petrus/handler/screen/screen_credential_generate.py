"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
import base64
import json

import global_schema
from lib.credentials import CredentialGenerator
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from ui import screen_credential_generator


class ScreenCredentialGenerate(QtWidgets.QMainWindow, screen_credential_generator.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenCredentialGenerate, self).__init__(*args, **kwargs)
        self.cred_loc = None
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

    @pyqtSlot()
    def on_btn_gen_clicked(self):
        # Obtaining the API key and OAUTH2.0 token input strings.
        api_key_gh = self.field_api_gh.text()
        api_key_yt = self.field_api_yt.text()
        drive_oauth_token_path = self.cred_loc
        decryption_password = self.field_pass.text()

        # Creating the base64 WordPress authorization key. [7]
        wp_user = self.field_api_wp_user.text()
        wp_pass = self.field_api_wp_pass.text()
        b64_wp_token = (base64.b64encode(f'{wp_user}:{wp_pass}'.encode())).decode('UTF-8')

        # Preparing the dict data.
        a = {}

        try:
            # Creating the credential dict structure.
            with open(drive_oauth_token_path, 'r') as b:
                a = {
                    'api_github': api_key_gh,
                    'api_youtube': api_key_yt,
                    'authorized_drive_oauth': json.load(b),
                    'wp_authorization': b64_wp_token,
                }

                # Now encrypt the JSON data.
                generator = CredentialGenerator()

                # Open the animation window and disable all elements in this window, to prevent user input.
                global_schema.anim.clear_and_show()
                global_schema.disable_widget(self)

                # Using multithreading to prevent GUI freezing [9]
                t = ThreadWithResult(target=generator.encrypt, args=(a, decryption_password,))
                t.start()
                while True:
                    if getattr(t, 'result', None):
                        # Obtaining the thread function's result
                        encrypted_bytes = t.result
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

                # Ask the user wherein this credential should be stored.
                # (Qt5 has built-in overwrite confirmation dialog.)
                ff = 'Encrypted JSON file (*.json.enc)'
                stored_cred = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Save the encrypted JSON credential into ...', '', ff)[0]

                if stored_cred == '':
                    # Report user cancelled operation.
                    QtWidgets.QMessageBox.information(
                        self, 'Operation Cancelled!', 'You have decided not to store the generated credential.',
                        QtWidgets.QMessageBox.Ok
                    )

                else:
                    stored_cred = stored_cred + '.json.enc' if not stored_cred.endswith('.json.enc') else stored_cred
                    Lg('main.ScreenCredentialGenerate.on_btn_gen_clicked',
                       f'Generating encrypted JSON into: {stored_cred} ...')

                    # Save the file.
                    with open(stored_cred, 'wb') as fo:
                        fo.write(encrypted_bytes)

                    # Report successful writing.
                    QtWidgets.QMessageBox.information(
                        self, 'Success!', f'Secure Simon Petrus credential has been generated to: {stored_cred}',
                        QtWidgets.QMessageBox.Ok
                    )

        except json.decoder.JSONDecodeError as e:
            QtWidgets.QMessageBox.warning(
                self, 'Error Detected!', f'{drive_oauth_token_path} is not a valid JSON file!: {e}',
                QtWidgets.QMessageBox.Ok
            )
            return
        except UnicodeDecodeError as e:
            QtWidgets.QMessageBox.warning(
                self, 'Error Detected!', f'{drive_oauth_token_path} is not a valid JSON file!: {e}',
                QtWidgets.QMessageBox.Ok
            )
            return
        except TypeError as e:
            QtWidgets.QMessageBox.warning(
                self, 'Error Detected!', f'You must specify a JSON file for the Google Drive OAUTH2.0 token: {e}',
                QtWidgets.QMessageBox.Ok
            )
            return
        except FileNotFoundError as e:
            QtWidgets.QMessageBox.warning(
                self, 'Error Detected!', f'You must specify a JSON file for the Google Drive OAUTH2.0 token: {e}',
                QtWidgets.QMessageBox.Ok
            )
            return

    @pyqtSlot()
    def on_btn_json_oauth_drive_clicked(self):
        ff = 'JSON file (*.json)'
        self.cred_loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Import the Google Drive OAUTH2.0 JSON file from ...', '', ff)[0]
        self.txt_cred_loc.setText(self.cred_loc)
        self.txt_cred_loc.setToolTip(self.cred_loc)
