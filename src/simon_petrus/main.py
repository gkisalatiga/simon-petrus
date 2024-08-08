"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] Dynamic loading of .ui files in Python
    - https://github.com/eyllanesc/stackoverflow/tree/master/questions/53899209
    - https://stackoverflow.com/a/53926554
    [2] "on_..._clicked()" functions are automatically connected to the respective slot
    - https://forum.qt.io/post/522391
    [3] Use "@pyqtSlot()" to prevent the slot from firing twice
    - https://stackoverflow.com/a/77741959
    [4] Remove all child items from a layout
    - https://stackoverflow.com/a/9375273
    - https://stackoverflow.com/a/9383780
    [5] Prevents GUI freezing
    - https://www.xingyulei.com/post/qt-threading/index.html
    [6] AES encryption of strings
    - https://onboardbase.com/blog/aes-encryption-decryption
    - https://github.com/Legrandin/pycryptodome
    [7] WordPress REST API references
    - https://medium.com/@vicgupta/how-to-upload-a-post-or-image-to-wordpress-using-rest-api-220fe046ff7a
"""

from Crypto.Cipher import AES
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import base64
import json
import os
import sys

from lib.credentials import CredentialGenerator
from lib.credentials import CredentialValidator
from lib.database import AppDatabase
from lib.logger import Logger as Lg
from lib.preferences import SavedPreferences
from lib.string_validator import StringValidator
from lib.uploader import Uploader
from ui import frame_liturgi_upload
from ui import frame_renungan
from ui import frame_social_media
from ui import frame_warta_upload
from ui import screen_credential_decrypt
from ui import screen_credential_generator
from ui import screen_main

# Initializes the app's internal saved preferences (global variable).
prefs = SavedPreferences()
prefs.init_configuration()

# Initializes the app's internal database (global variable).
app_db = AppDatabase(prefs)


class ScreenCredentialDecrypt(QtWidgets.QMainWindow, screen_credential_decrypt.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenCredentialDecrypt, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # The temporary value of the selected credential location.
        self.cred_loc = ''

        # Whether there is a saved credential location.
        if prefs.settings['remember_cred_loc'] == 1 and prefs.settings['saved_cred_loc'] != '':
            self.cred_loc = prefs.settings['saved_cred_loc']
            self.chk_save_cred_loc.setChecked(True)
            self.txt_cred_loc.setText(prefs.settings['saved_cred_loc'])
            self.txt_cred_loc.setToolTip(prefs.settings['saved_cred_loc'])

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
        self.cred_loc = QtWidgets.QFileDialog.getOpenFileName(self, 'Import admin credential file from ...', '', ff)[0]
        self.txt_cred_loc.setText(self.cred_loc)
        self.txt_cred_loc.setToolTip(self.cred_loc)

    @pyqtSlot()
    def on_btn_decrypt_clicked(self):
        # Whether to save the credential location.
        if self.chk_save_cred_loc.isChecked() and self.cred_loc != '':
            prefs.settings['remember_cred_loc'] = 1
            prefs.settings['saved_cred_loc'] = self.txt_cred_loc.text()
        else:
            prefs.settings['remember_cred_loc'] = 0
            prefs.settings['saved_cred_loc'] = ''

        # Save the settings.
        prefs.save_config()

        # Change the status.
        self.label_status.setText('Attempting to decrypt the credential data ...')
        QtCore.QCoreApplication.processEvents()

        # Validate the input credential file, and attempt to decrypt the input bytes.
        password_key = self.field_cred.text()
        validator = CredentialValidator(self.cred_loc)
        is_valid, decrypted_dict, message = validator.decrypt(password_key)

        # Display whatever status message returned from the decryption to the user.
        msg_title = 'Decryption successful!' if is_valid else 'Failed to decrypt the credential data!'
        self.label_status.setText(msg_title)
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMessageBox.warning(
            self, msg_title, message,
            QtWidgets.QMessageBox.Ok
        )

        if is_valid:
            app_db.populate_credentials(decrypted_dict)

            # Preparing the JSON schema, ensuring that we have a valid data.
            app_db.load_json_schema()
            if not app_db.is_db_exist or not app_db.is_db_valid:
                app_db.refresh_json_schema()

            # Open the control panel (administrator dashboard).
            self.hide()
            ScreenMain(self).show()

    @pyqtSlot()
    def on_btn_exit_clicked(self):
        self.close()

    @pyqtSlot()
    def on_btn_show_pass_clicked(self):
        if self.field_cred.echoMode() == QtWidgets.QLineEdit.Password:
            self.field_cred.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.field_cred.setEchoMode(QtWidgets.QLineEdit.Password)


class ScreenCredentialGenerate(QtWidgets.QMainWindow, screen_credential_generator.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenCredentialGenerate, self).__init__(*args, **kwargs)
        self.cred_loc = None
        self.setupUi(self)

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
                encrypted_bytes = generator.encrypt(a, decryption_password)

                # Ask the user wherein this credential should be stored.
                # (Qt5 has built-in overwrite confirmation dialog.)
                ff = 'Encrypted JSON file (*.json.enc)'
                stored_cred = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Save the encrypted JSON credential into ...', '', ff)[0]
                if stored_cred == '':
                    return
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


class ScreenMain(QtWidgets.QMainWindow, screen_main.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenMain, self).__init__(*args, **kwargs)
        self.setupUi(self)

    def clear_fragment_layout_content(self):
        """
        This function removes every child element from the GridLayout that is used
        to display the fragments. [4]
        :return: nothing.
        """
        for i in range(self.fragment_layout.count()):
            item = self.fragment_layout.itemAt(i).widget()
            item.deleteLater()

    @pyqtSlot()
    def on_btn_sync_clicked(self):
        is_success = app_db.refresh_json_schema()
        if is_success:
            QtWidgets.QMessageBox.information(
                self, 'Berhasil menyinkronisasi!',
                'Data JSON dari repositori utama GKI Salatiga+ berhasil dimuat.',
                QtWidgets.QMessageBox.Ok
            )

            # Load the latest downloaded JSON schema into the app.
            app_db.load_json_schema()

    @pyqtSlot()
    def on_cmd_liturgi_clicked(self):
        frame = QtWidgets.QFrame()
        fragment = FrameTataIbadah()
        fragment.setupUi(frame)

        # Displaying the frame
        self.clear_fragment_layout_content()
        self.fragment_layout.addWidget(fragment)

        # Prevents freezing [5]
        QtCore.QCoreApplication.processEvents()
        pass

    @pyqtSlot()
    def on_cmd_renungan_clicked(self):
        frame = QtWidgets.QFrame()
        fragment = FrameRenungan()
        fragment.setupUi(frame)

        # Displaying the frame
        self.clear_fragment_layout_content()
        self.fragment_layout.addWidget(fragment)

        # Prevents freezing [5]
        QtCore.QCoreApplication.processEvents()
        pass

    @pyqtSlot()
    def on_cmd_social_media_clicked(self):
        frame = QtWidgets.QFrame()
        fragment = FrameSocialMedia()
        fragment.setupUi(frame)

        # Displaying the frame
        self.clear_fragment_layout_content()
        self.fragment_layout.addWidget(fragment)

        # Prevents freezing [5]
        QtCore.QCoreApplication.processEvents()
        pass

    @pyqtSlot()
    def on_cmd_warta_clicked(self):
        frame = QtWidgets.QFrame()
        fragment = FrameWartaJemaat()
        fragment.setupUi(frame)

        # Displaying the frame
        self.clear_fragment_layout_content()
        self.fragment_layout.addWidget(fragment)

        # Prevents freezing [5]
        QtCore.QCoreApplication.processEvents()
        pass


class FrameRenungan(QtWidgets.QFrame, frame_renungan.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameRenungan, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Pre-fill the input fields with the data already present in the JSON schema.
        self.field_kiddy.setText(app_db.db['ykb'][0]['url'])
        self.field_teens.setText(app_db.db['ykb'][1]['url'])
        self.field_youth.setText(app_db.db['ykb'][2]['url'])
        self.field_wasiat.setText(app_db.db['ykb'][3]['url'])
        self.field_lansia.setText(app_db.db['ykb'][4]['url'])

    @pyqtSlot()
    def on_btn_save_clicked(self):
        app_db.db['ykb'][0]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_kiddy').text()
        app_db.db['ykb'][1]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_teens').text()
        app_db.db['ykb'][2]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_youth').text()
        app_db.db['ykb'][3]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_wasiat').text()
        app_db.db['ykb'][4]['url'] = self.findChild(QtWidgets.QLineEdit, 'field_lansia').text()

        # Save to local file.
        app_db.save_local()

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )


class FrameSocialMedia(QtWidgets.QFrame, frame_social_media.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameSocialMedia, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Pre-fill the input fields with the data already present in the JSON schema.
        self.field_email.setText(app_db.db['url-profile']['email'])
        self.field_fb.setText(app_db.db['url-profile']['fb'])
        self.field_ig.setText(app_db.db['url-profile']['insta'])
        self.field_wa.setText(app_db.db['url-profile']['whatsapp'])
        self.field_web.setText(app_db.db['url-profile']['web'])
        self.field_yt.setText(app_db.db['url-profile']['youtube'])

    @pyqtSlot()
    def on_btn_save_clicked(self):
        app_db.db['url-profile']['email'] = self.findChild(QtWidgets.QLineEdit, 'field_email').text()
        app_db.db['url-profile']['fb'] = self.findChild(QtWidgets.QLineEdit, 'field_fb').text()
        app_db.db['url-profile']['insta'] = self.findChild(QtWidgets.QLineEdit, 'field_ig').text()
        app_db.db['url-profile']['whatsapp'] = self.findChild(QtWidgets.QLineEdit, 'field_wa').text()
        app_db.db['url-profile']['web'] = self.findChild(QtWidgets.QLineEdit, 'field_web').text()
        app_db.db['url-profile']['youtube'] = self.findChild(QtWidgets.QLineEdit, 'field_yt').text()

        # Save to local file.
        app_db.save_local()

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )


class FrameTataIbadah(QtWidgets.QFrame, frame_liturgi_upload.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameTataIbadah, self).__init__(*args, **kwargs)
        self.localized_date = None
        self.pdf_loc = None
        self.setupUi(self)

        # Trigger the rendering of initial value.
        self.on_date_picker_date_time_changed()

        self.date_picker.dateTimeChanged.connect(self.on_date_picker_date_time_changed)

    @pyqtSlot()
    def on_date_picker_date_time_changed(self):
        cur_date = self.findChild(QtWidgets.QDateEdit, 'date_picker').text().split('/')
        cur_date_int = []
        for l in cur_date:
            cur_date_int.append(int(l))

        # Validate the current date string.
        cur_month_name = StringValidator.LOCALE_MONTH_NAME[cur_date_int[1] - 1]

        # Get day of the week string.
        int_day_of_week = StringValidator().get_day_of_week(cur_date_int[2], cur_date_int[1], cur_date_int[0])
        cur_day_of_week = StringValidator.LOCALE_DAY_OF_WEEK[int_day_of_week]

        # Print the date snippet.
        str_date = f'{cur_day_of_week}, {cur_date_int[0]} {cur_month_name} 20{cur_date[2]}'
        self.findChild(QtWidgets.QLabel, 'txt_date_format').setText(str_date)

        # Store the properly formated and localized date, which will become the post title.
        self.localized_date = f'{cur_date_int[0]} {cur_month_name} 20{cur_date[2]}'

    @pyqtSlot()
    def on_btn_pdf_select_clicked(self):
        ff = 'Portable Document Format (*.pdf)'
        self.pdf_loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih berkas PDF tata ibadah untuk diunggah', '', ff)[0]

        # Display the currently selected PDF file for uploading.
        pdf_basename = os.path.basename(self.pdf_loc)
        self.findChild(QtWidgets.QLabel, 'txt_pdf_loc').setText(pdf_basename)
        self.findChild(QtWidgets.QLabel, 'txt_pdf_loc').setToolTip(self.pdf_loc)

    @pyqtSlot()
    def on_btn_upload_clicked(self):
        # Determining the post title.
        post_title = f'Tata Ibadah {self.localized_date}'

        # Display preamble status.
        self.findChild(QtWidgets.QLabel, 'label_status').setText("Sedang mengunggah tata ibadah ...")
        QtCore.QCoreApplication.processEvents()

        # Begin uploading the PDF.
        uploader = Uploader(prefs, app_db)
        is_success, msg = uploader.upload_liturgi(self.pdf_loc, post_title)

        # Display the status information.
        # Display whatever status message returned from the decryption to the user.
        msg_title = 'Berhasil mengunggah tata ibadah!' if is_success else 'Gagal mengunggah tata ibadah!'
        self.findChild(QtWidgets.QLabel, 'label_status').setText(msg_title)
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMessageBox.warning(
            self, msg_title, msg,
            QtWidgets.QMessageBox.Ok
        )


class FrameWartaJemaat(QtWidgets.QFrame, frame_warta_upload.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameWartaJemaat, self).__init__(*args, **kwargs)
        self.localized_date = None
        self.pdf_loc = None
        self.setupUi(self)

        # Trigger the rendering of initial value.
        self.on_date_picker_date_time_changed()

        self.date_picker.dateTimeChanged.connect(self.on_date_picker_date_time_changed)

    @pyqtSlot()
    def on_date_picker_date_time_changed(self):
        cur_date = self.findChild(QtWidgets.QDateEdit, 'date_picker').text().split('/')
        cur_date_int = []
        for l in cur_date:
            cur_date_int.append(int(l))

        # Validate the current date string.
        cur_month_name = StringValidator.LOCALE_MONTH_NAME[cur_date_int[1] - 1]

        # Get day of the week string.
        int_day_of_week = StringValidator().get_day_of_week(cur_date_int[2], cur_date_int[1], cur_date_int[0])
        cur_day_of_week = StringValidator.LOCALE_DAY_OF_WEEK[int_day_of_week]

        # Print the date snippet.
        str_date = f'{cur_day_of_week}, {cur_date_int[0]} {cur_month_name} 20{cur_date[2]}'
        self.findChild(QtWidgets.QLabel, 'txt_date_format').setText(str_date)

        # Store the properly formated and localized date, which will become the post title.
        self.localized_date = f'{cur_date_int[0]} {cur_month_name} 20{cur_date[2]}'

    @pyqtSlot()
    def on_btn_pdf_select_clicked(self):
        ff = 'Portable Document Format (*.pdf)'
        self.pdf_loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih berkas PDF warta jemaat untuk diunggah', '', ff)[0]

        # Display the currently selected PDF file for uploading.
        pdf_basename = os.path.basename(self.pdf_loc)
        self.findChild(QtWidgets.QLabel, 'txt_pdf_loc').setText(pdf_basename)
        self.findChild(QtWidgets.QLabel, 'txt_pdf_loc').setToolTip(self.pdf_loc)

    @pyqtSlot()
    def on_btn_upload_clicked(self):
        # Determining the post title.
        post_title = f'Warta Jemaat {self.localized_date}'

        # Display preamble status.
        self.findChild(QtWidgets.QLabel, 'label_status').setText("Sedang mengunggah warta jemaat ...")
        QtCore.QCoreApplication.processEvents()

        # Begin uploading the PDF.
        uploader = Uploader(prefs, app_db)
        is_success, msg = uploader.upload_warta(self.pdf_loc, post_title)

        # Display the status information.
        # Display whatever status message returned from the decryption to the user.
        msg_title = 'Berhasil mengunggah warta jemaat!' if is_success else 'Gagal mengunggah warta jemaat!'
        self.findChild(QtWidgets.QLabel, 'label_status').setText(msg_title)
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMessageBox.warning(
            self, msg_title, msg,
            QtWidgets.QMessageBox.Ok
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = ScreenCredentialDecrypt()
    win.show()

    # Actually exiting the app.
    exit_code = app.exec()

    # Performing post-operation procedures.
    prefs.shutdown()

    # Appropriately exiting the app.
    sys.exit(exit_code)
