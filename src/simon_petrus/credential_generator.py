"""
Simon Petrus - Credential Generator
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] AES encryption of strings
    - https://onboardbase.com/blog/aes-encryption-decryption
"""
import os.path

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import hashlib
import json
import pyargon2
import sys

import credential_generator_ui


class WindowMain(QtWidgets.QMainWindow, credential_generator_ui.Ui_MainWindow):

    GEN_CREDENTIAL_SEPARATOR = get_random_bytes(4)
    GEN_PASSWORD_PEPPER = 'V]=tDk$3<=_qA2TR'
    GEN_PASSWORD_SALT = hashlib.sha512(get_random_bytes(32))

    def __init__(self, *args, obj=None, **kwargs):
        super(WindowMain, self).__init__(*args, **kwargs)
        self.cred_loc = None
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_gen_clicked(self):
        api_key_gh = self.field_api_gh.text()
        api_key_wp = self.field_api_wp.text()
        api_key_yt = self.field_api_yt.text()
        drive_oauth_token_path = self.cred_loc
        decrypt_password = self.field_pass.text()

        try:
            # Creating the credential dict structure.
            a = {}
            with open(drive_oauth_token_path, 'r') as b:
                a = {
                    'api_github': api_key_gh,
                    'api_wordpress': api_key_wp,
                    'api_youtube': api_key_yt,
                    'authorized_drive_oauth': json.load(b)
                }
        except json.decoder.JSONDecodeError:
            QtWidgets.QMessageBox.warning(
                self, 'Error Detected!', f'{drive_oauth_token_path} is not a valid JSON file!',
                QtWidgets.QMessageBox.Ok
            )
            return
        except TypeError:
            QtWidgets.QMessageBox.warning(
                self, 'Error Detected!', f'You must specify a JSON file for the Google Drive OAUTH2.0 token.',
                QtWidgets.QMessageBox.Ok
            )
            return

        # Convert the user's input password into a 16-bytes Argon2 hash.
        key = pyargon2.hash(decrypt_password,
                            salt=self.GEN_PASSWORD_SALT.hexdigest(),
                            pepper=self.GEN_PASSWORD_PEPPER,
                            variant='id',
                            memory_cost=2**12,
                            time_cost=1000,
                            parallelism=10,
                            hash_len=16,
                            encoding='raw',
                            )

        # GCM (Galois Counter Mode) is the most secure mode, [1]
        # but AES-OFB is less complex to implement.
        cipher = AES.new(bytes(key), AES.MODE_OFB)
        cipher_text = cipher.encrypt(str(a).encode())
        iv = cipher.iv

        # Generate the output binary blob.
        sep = self.GEN_CREDENTIAL_SEPARATOR
        out = sep + cipher_text + sep + iv + sep + self.GEN_PASSWORD_SALT.digest()

        # DEBUG. Please always comment out on production.
        # ---
        # This is the output, encrypted byte string.
        '''print(cipher_text, iv, self.GEN_PASSWORD_SALT)
        print('==' * 25)
        print(out)
        print('==' * 25)
        print(out.split(sep))
        print('==' * 25)
        print(out[:4])
        print('==' * 25)
        print(sep)'''

        # Ask the user wherein this credential should be stored.
        # (Qt5 has built-in overwrite confirmation dialog.)
        ff = 'Encrypted JSON file (*.json.enc)'
        stored_cred = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save the encrypted JSON credential into ...', '', ff)[0]
        if stored_cred == '':
            return
        else:
            stored_cred = stored_cred + '.json.enc' if not stored_cred.endswith('.json.enc') else stored_cred

        # DEBUG. Please always comment out on production.
        # print(stored_cred)

        # Save the file.
        with open(stored_cred, 'wb') as fo:
            fo.write(out)

    @pyqtSlot()
    def on_btn_json_oauth_drive_clicked(self):
        ff = 'JSON file (*.json)'
        self.cred_loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Import the Google Drive OAUTH2.0 JSON file from ...', '', ff)[0]
        self.txt_cred_loc.setText(self.cred_loc)
        self.txt_cred_loc.setToolTip(self.cred_loc)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    win = WindowMain()
    win.show()
    app.exec()
