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
    [8] Playing GIF images in PyQt5
    - https://stackoverflow.com/q/10261265
    - https://www.perplexity.ai/search/qtdesigner-python-displaying-g-cPTPIewkRHS1213kS0t2nQ
    [9] PyQt5 multithreading to prevent screen freeze
    - https://stackoverflow.com/a/65447493
    - https://github.com/shailshouryya/save-thread-result
    [10] Prevent window resizing in PyQt5
    - https://stackoverflow.com/a/13775478
    [11] Capitalize the first letter of words in a sentence
    - https://stackoverflow.com/a/1549644
    [12] Displaying image in PyQt5
    - https://stackoverflow.com/a/51431109
    [13] Sorting a QListWidget element.
    - https://www.geeksforgeeks.org/pyqt5-qlistwidget-making-sorting-enabled/
    [14] Detecting the mime type of a file
    - https://stackoverflow.com/a/2753385
"""

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import pyqtSlot, QPoint, pyqtSignal, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime as dt
from magic import Magic as Mgc
from urllib import request
import base64
import copy
import json
import os
import sys
import time
import urllib

from lib.assets import AppAssets
from lib.credentials import CredentialGenerator
from lib.credentials import CredentialValidator
from lib.database import AppDatabase
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from lib.preferences import SavedPreferences
from lib.string_validator import StringValidator
from lib.uploader import Uploader
from loading_animation import ScreenLoadingAnimation
from ui import dialog_agenda
from ui import dialog_banner
from ui import dialog_carousel
from ui import dialog_forms
from ui import dialog_persembahan
from ui import dialog_poster
from ui import frame_agenda
from ui import frame_carousel
from ui import frame_carousel_article
from ui import frame_carousel_poster
from ui import frame_carousel_yt
from ui import frame_default
from ui import frame_formulir
from ui import frame_liturgi_upload
from ui import frame_persembahan
from ui import frame_renungan
from ui import frame_social_media
from ui import frame_warta_upload
from ui import frame_wp_homepage
from ui import screen_credential_decrypt
from ui import screen_credential_generator
from ui import screen_main
from ui import screen_settings
from ui import screen_test

# DEBUG: For testing variable change and remembered states.
debug_int_value = 0

# Initializes the app's internal saved preferences (global variable).
prefs = SavedPreferences()
prefs.init_configuration()

# Initializes the app's internal database (global variable).
app_db = AppDatabase(prefs)

# Initializes the app's assets manager.
app_assets = AppAssets(prefs, app_db)


def disable_widget(qt_widget: QtWidgets.QWidget):
    """
    This function will disable all elements inside a given QtWidget, including the widget itself.
    :param qt_widget: the QWidget whose children will be disabled.
    :return: nothing.
    """
    qt_widget.setEnabled(False)


def enable_widget(qt_widget: QtWidgets.QWidget):
    """
    This function will enable all elements inside a given QtWidget, including the widget itself.
    :param qt_widget: the QWidget whose children will be enabled.
    :return: nothing.
    """
    qt_widget.setEnabled(True)


def push_all_data():
    """
    This function pushes the JSON schemas as well as the individual carousel, static HTML,
    and custom images data.
    :param anim: the animator window.
    :return: the "app_db.push_json_schema"'s return value, anything it is.
    """
    # Ensures the latest temporary JSON dict is retrieved.
    app_assets.db = app_db.db

    # Round one: uploading the assets data.
    is_success, j_1, msg = app_assets.push_assets(anim)
    if not is_success:
        return is_success, j_1, msg

    # Round two: uploading the JSON schema.
    is_success, j_2, msg = app_db.push_json_schema(anim)
    if not is_success:
        return is_success, j_2, msg

    # Final return: if successful.
    msg = 'All assets data and JSON schema have been uploaded and committed successfully!'
    return True, (j_1, j_2), msg


def refresh_all_data():
    """
    This function refreshes all data used in this app, from the main JSON schema
    to the carousel, custom images, and static HTML.
    :return: True (not significant, but it is expressed so that the multithreader won't freeze infinitely).
    """
    app_db.refresh_json_schema()
    app_assets.get_carousel()
    app_assets.get_main_qris()
    return True


class ScreenCredentialDecrypt(QtWidgets.QMainWindow, screen_credential_decrypt.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenCredentialDecrypt, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

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
        loc = QtWidgets.QFileDialog.getOpenFileName(self, 'Import admin credential file from ...', '', ff)[0]
        if not loc == '':
            self.cred_loc = loc
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
        validator = CredentialValidator(anim, self.cred_loc)

        # Open the animation window and disable all elements in this window, to prevent user input.
        anim.clear_and_show()
        disable_widget(self)

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
        enable_widget(self)
        anim.hide()

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

            # Adjust the credentials of the assets manager.
            app_assets.set_credentials(app_db.credentials)

            # Preparing the JSON schema, ensuring that we have a valid data.
            app_db.load_json_schema()

            # If we do not have a valid JSON schema, attempt to refresh from GitHub repo.
            if not app_db.is_db_exist or not app_db.is_db_valid or prefs.settings['autosync_on_launch'] == 1:

                # Disable all elements in this window for a while, to prevent user input.
                disable_widget(self)

                # Using multithreading to prevent GUI freezing [9]
                t = ThreadWithResult(target=refresh_all_data, args=())
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
                enable_widget(self)

            # Open the control panel (administrator dashboard).
            self.hide()
            # ScreenMain(self).show()
            global win_main
            win_main = ScreenMain(self)
            win_main.show()

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
                generator = CredentialGenerator(anim)

                # Open the animation window and disable all elements in this window, to prevent user input.
                anim.clear_and_show()
                disable_widget(self)

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
                enable_widget(self)
                anim.hide()

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


class ScreenMain(QtWidgets.QMainWindow, screen_main.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenMain, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Displaying the default fragment.
        self.clear_fragment_and_display(cur_fragment)

    def clear_fragment_layout_content(self):
        """
        This function removes every child element from the GridLayout that is used
        to display the fragments. [4]
        :return: nothing.
        """
        for i in range(self.fragment_layout.count()):
            item = self.fragment_layout.itemAt(i).widget()
            item.deleteLater()

    def clear_fragment_and_display(self, fragment_str: str):
        """
        This function clears the currently fragment and replace it with a new one automatically.
        :param fragment_str: the target fragment to display, as defined in the local fragment dictionary.
        :return: nothing.
        """
        # Prevents freezing [5]
        QtCore.QCoreApplication.processEvents()

        # The fragment dictionary.
        const_fragment_dictionary = {
            'fragment_agenda': FrameAgenda(),
            'fragment_carousel': FrameCarousel(),
            'fragment_default': FrameDefault(),
            'fragment_formulir': FrameFormulir(),
            'fragment_persembahan': FramePersembahan(),
            'fragment_renungan': FrameRenungan(),
            'fragment_social_media': FrameSocialMedia(),
            'fragment_tata_ibadah': FrameTataIbadah(),
            'fragment_warta_jemaat': FrameWartaJemaat(),
            'fragment_wp_home': FrameWordPressHome()
        }

        # Prepare the fragment.
        fragment = const_fragment_dictionary[fragment_str]

        # Clear the previous fragment.
        self.clear_fragment_layout_content()

        # Preparing the fragment to display.
        frame = QtWidgets.QFrame()
        fragment.setupUi(frame)

        # Displaying the frame
        self.fragment_layout.addWidget(fragment)

    @pyqtSlot()
    def on_action_exit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_action_settings_triggered(self):
        ScreenSettings(self).show()

    @pyqtSlot()
    def on_btn_push_clicked(self):
        # Display the confirmation dialog.
        confirmation_res = QMessageBox.question(
            self,
            'Unggah Pembaruan GKI Salatiga+',
            'Apakah Anda yakin akan mengunggah perubahan lokal ke repositori awan GKI Salatiga+?\n'
            'Perubahan yang sudah dibuat tidak dapat dikembalikan ke kondisi awal.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        # Carry out the repo push.
        if confirmation_res == QMessageBox.Yes:

            # Open the animation window and disable all elements in this window, to prevent user input.
            anim.clear_and_show()
            global win_main
            disable_widget(win_main)

            # Using multithreading to prevent GUI freezing [9]
            t = ThreadWithResult(target=push_all_data, args=())
            t.start()
            while True:
                if getattr(t, 'result', None):
                    # Obtaining the thread function's result
                    is_success, _, msg = t.result
                    t.join()

                    break
                else:
                    # When this block is reached, it means the function has not returned any value
                    # While we wait for the thread response to be returned, let us prevent
                    # Qt5 GUI freezing by repeatedly executing the following line:
                    QtCore.QCoreApplication.processEvents()

            # Closing the loading animation and re-enable the window.
            enable_widget(win_main)
            anim.hide()

            # Display the status information.
            # Display whatever status message returned from the decryption to the user.
            msg_title = 'Berhasil mengunggah pembaruan data GKI Salatiga+!' if is_success else 'Gagal melakukan pemutakhiran data GKI Salatiga+!'
            QtWidgets.QMessageBox.warning(
                self, msg_title, msg,
                QtWidgets.QMessageBox.Ok
            )

            # Save the successfully pushed data locally.
            # (Commented out because it causes the "update-count" metadata to double.
            '''if is_success:
                app_db.save_local()'''

    @pyqtSlot()
    def on_btn_sync_clicked(self):
        # Open the animation window and disable all elements in this window, to prevent user input.
        anim.clear_and_show()
        global win_main
        disable_widget(win_main)

        # Fake the progression.
        msg = 'Menyinkronisasi basis data JSON dan berkas aset dari repositori GitHub ...'
        anim.set_prog_msg(50, msg)
        Lg('main.ScreenMain.on_btn_sync_clicked', msg)

        # Using multithreading to prevent GUI freezing [9]
        t = ThreadWithResult(target=refresh_all_data, args=())
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                is_success = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Closing the loading animation and re-enable the window.
        enable_widget(win_main)
        anim.hide()

        if is_success:
            QtWidgets.QMessageBox.information(
                self, 'Berhasil menyinkronisasi!',
                'Data JSON dari repositori utama GKI Salatiga+ berhasil dimuat.',
                QtWidgets.QMessageBox.Ok
            )

            # Load the latest downloaded JSON schema into the app.
            app_db.load_json_schema()

            # Refresh the Qt widget of the currently active fragment.
            global cur_fragment
            self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_agenda_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_agenda'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_carousel_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_carousel'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_formulir_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_formulir'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_liturgi_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_tata_ibadah'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_persembahan_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_persembahan'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_renungan_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_renungan'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_social_media_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_social_media'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_warta_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_warta_jemaat'
        self.clear_fragment_and_display(cur_fragment)

    @pyqtSlot()
    def on_cmd_wp_home_clicked(self):
        global cur_fragment
        cur_fragment = 'fragment_wp_home'
        self.clear_fragment_and_display(cur_fragment)


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


class DialogBanner(QtWidgets.QDialog, dialog_banner.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogBanner, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())


class DialogCarousel(QtWidgets.QDialog, dialog_carousel.Ui_Dialog):

    # Some type constants.
    CAROUSEL_TYPE_POSTER = 'poster'
    CAROUSEL_TYPE_URL = 'article'
    CAROUSEL_TYPE_YOUTUBE = 'yt'

    # This associates "const_carousel_fragment_dictionary" with the respective int.
    CONST_CAROUSEL_FRAGMENT_INT = [
        'fragment_carousel_poster',
        'fragment_carousel_yt',
        'fragment_carousel_article'
    ]

    # This associates JSON's type constants with the respective int.
    CONST_CAROUSEL_TYPE_INT = [
        'poster',
        'yt',
        'article'
    ]

    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogCarousel, self).__init__(*args, **kwargs)
        self.action = None
        self.carousel_dict = None
        self.carousel_key = None
        self.cur_frame_obj = QtWidgets.QFrame()
        self.cur_idx = 0
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Connecting action slots.
        self.carousel_type.currentIndexChanged.connect(self.on_carousel_type_index_changed)

    def clear_fragment_and_display(self, fragment_str: str):
        """
        This function clears the current fragment and replace it with a new one automatically.
        :param fragment_str: the target fragment to display, as defined in the local fragment dictionary.
        :return: nothing.
        """
        # Prevents freezing [5]
        QtCore.QCoreApplication.processEvents()

        # DEBUG.
        # print('FRAGMENT_STR: ', fragment_str)

        # DEBUG. This is to test out accessing child elements in nested frames.
        # Please always comment out.
        # global debug_int_value
        # debug_int_value += 1
        # cur_frame = self.findChild(QtWidgets.QGridLayout, 'fragment_layout').itemAt(0)
        # cur_obj_name = cur_frame.widget().objectName()
        # print(cur_frame)
        # print(cur_obj_name)

        # The fragment dictionary.
        const_carousel_fragment_dictionary = {
            'fragment_carousel_poster': FrameCarouselPoster(),
            'fragment_carousel_yt': FrameCarouselYouTube(),
            'fragment_carousel_article': FrameCarouselArticle()
        }

        # Prepare the fragment.
        fragment = const_carousel_fragment_dictionary[fragment_str]

        # Clear the previous fragment.
        self.clear_fragment_layout_content()

        # Preparing the fragment to display.
        frame = QtWidgets.QFrame()
        fragment.setupUi(frame)

        # Connect this fragment with this dialog's button box.
        btn_box = self.findChild(QtWidgets.QDialogButtonBox, 'button_box')
        fragment.set_parent_button_box(btn_box)

        # DEBUG.
        # print('CHILDREN_COUNT (BEFORE): ', self.fragment_layout.count())

        # Displaying the frame
        self.fragment_layout.addWidget(fragment)

        # DEBUG.
        # print('CHILDREN_COUNT (AFTER): ', self.fragment_layout.count())

        # Obtain the latest element's index of the grid layout.
        last_idx = self.fragment_layout.count() - 1

        # Saving the child frame/fragment object.
        # self.cur_frame_obj = self.findChild(QtWidgets.QGridLayout, 'fragment_layout').itemAt(0).widget()
        self.cur_frame_obj = self.findChild(QtWidgets.QGridLayout, 'fragment_layout').itemAt(last_idx).widget()

        # Perform early data validation.
        self.cur_frame_obj.validate_fields()

    def clear_fragment_layout_content(self):
        """
        This function removes every child element from the GridLayout that is used
        to display the fragments. [4]
        :return: nothing.
        """
        for i in range(self.fragment_layout.count()):
            item = self.fragment_layout.itemAt(i).widget()
            item.deleteLater()

    def on_carousel_type_index_changed(self):
        self.cur_idx = self.findChild(QtWidgets.QComboBox, 'carousel_type').currentIndex()

        # Displaying the right fragment.
        self.clear_fragment_and_display(self.CONST_CAROUSEL_FRAGMENT_INT[self.cur_idx])

        # Ensures we have the prefilled date when the action is "new".
        self.prefill_fragment_elements()

    def populate_edit_data(self, carousel_key, carousel_dict):
        """
        Populate the current "edit" dialog state with a given existing carousel's data.
        :param carousel_key: the associated carousel key string.
        :param carousel_dict: the associated carousel data.
        :return: nothing.
        """
        self.carousel_key = carousel_key
        self.carousel_dict = carousel_dict

    def prefill_fragment_elements(self):
        """
        Prefill the currently active fragment's essential data.
        Only applies to "edit" actions.
        :return: nothing.
        """
        if not self.action == 'edit':

            # If the action is 'new', just prefill the creation date.
            if self.action == 'new':

                # Prepare the date string in "YYYY-MM-DD" format.
                now = dt.now()
                y = now.year
                m = now.month
                d = now.day
                preformatted_date = f'{y}-{self.zero_pad_date(m)}-{self.zero_pad_date(d)}'

                # Obtain the user-friendly date locale string.
                formatted_date = StringValidator.get_full_date(preformatted_date)

                # Display the preliminary date.
                self.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_date').setText(formatted_date)
                self.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_date').setToolTip(preformatted_date)

                return

        # DEBUG.
        # print('OBJ NAME: ', self.cur_frame_obj.objectName())
        # print('CAROUSEL TYPE: ', self.carousel_dict['type'])

        # Set the title and date, which is the same in all frames.
        title = self.carousel_dict['title']
        self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').setText(title)
        date = StringValidator.get_full_date(self.carousel_dict['date-created'])
        self.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_date').setText(date)

        # Preserve original JSON data.
        self.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_date').setToolTip(self.carousel_dict['date-created'])

        if self.carousel_dict['type'] == self.CAROUSEL_TYPE_POSTER:
            # Set the banner image location.
            banner_loc = app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + self.carousel_key + os.sep + \
                         self.carousel_dict['banner']
            banner_loc_short = os.path.split(banner_loc)[1]
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(banner_loc_short)
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(banner_loc)

            # Set the poster location.
            poster_loc = app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + self.carousel_key + os.sep + \
                         self.carousel_dict['poster-image']
            poster_loc_short = os.path.split(poster_loc)[1]
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_poster_loc').setText(poster_loc_short)
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_poster_loc').setToolTip(poster_loc)

            # Set the poster caption.
            caption = self.carousel_dict['poster-caption']
            self.cur_frame_obj.findChild(QtWidgets.QPlainTextEdit, 'txt_caption').setPlainText(caption)

        elif self.carousel_dict['type'] == self.CAROUSEL_TYPE_YOUTUBE:
            # Set the URL.
            url = self.carousel_dict['yt-link']
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_url').setText(url)

            # Obtain the YouTube-related metadata.
            yt_title = self.carousel_dict['yt-title']
            yt_date = StringValidator.get_full_date(self.carousel_dict['yt-date'])
            yt_thumb = self.carousel_dict['yt-thumbnail']
            yt_is_live = 'Live' if self.carousel_dict['yt-is_live'] == 1 else 'Pre-Recorded'
            yt_desc = self.carousel_dict['yt-desc']

            # Displaying the metadata.
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_yt_title').setText(yt_title)
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_yt_date').setText(yt_date)
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_yt_thumb').setText(yt_thumb)
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_yt_live').setText(yt_is_live)
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_yt_desc').setText(yt_desc)

            # Preserve original JSON data.
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_yt_date').setToolTip(self.carousel_dict['yt-date'])
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_yt_live').setToolTip(str(self.carousel_dict['yt-is_live']))

        elif self.carousel_dict['type'] == self.CAROUSEL_TYPE_URL:
            # Set the URL.
            url = self.carousel_dict['article-url']
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_url').setText(url)

            # Set the banner image location.
            banner_loc = app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + self.carousel_key + os.sep + \
                         self.carousel_dict['banner']
            banner_loc_short = os.path.split(banner_loc)[1]
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(banner_loc_short)
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(banner_loc)

        # At last, validate the child's data.
        self.validate_child_fragment()

    def set_action(self, action: str):
        """
        Determine the carousel action that this class should respond to.
        Possible values: 'new' and 'edit'
        :param action:
        :return:
        """
        self.action = action

    def validate_child_fragment(self):
        """ Validates the child fragment's user data in this dialog. """
        self.cur_frame_obj.validate_fields()

    def zero_pad_date(self, date_int: int):
        if date_int < 10:
            return f'0{date_int}'
        else:
            return str(date_int)


class DialogForms(QtWidgets.QDialog, dialog_forms.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogForms, self).__init__(*args, **kwargs)
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
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan judul dan tautan URL!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        elif not url.startswith('http') or not url.__contains__('://'):
            self.findChild(QtWidgets.QLabel, 'label_status').setText('URL Anda harus dimulai dengan "http://" atau "https://"!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(True)


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


class DialogPoster(QtWidgets.QDialog, dialog_poster.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogPoster, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())


class FrameAgenda(QtWidgets.QFrame, frame_agenda.Ui_Frame):

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    # The dict key for each day of the week.
    DAY_OF_WEEK_KEY = [
        'mon',
        'tue',
        'wed',
        'thu',
        'fri',
        'sat',
        'sun'
    ]

    def __init__(self, *args, obj=None, **kwargs):
        super(FrameAgenda, self).__init__(*args, **kwargs)
        self.action = None
        self.cur_day_int = 0  # --- the default.
        self.cur_item = None
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogAgenda(self)

        # Initiate inital values according to the original, non-edited JSON schema.
        self.agenda_dict = copy.deepcopy(app_db.db['agenda'])

        # Initialize the initial values.
        self.prefill_list_items()

        # Initialize the day title.
        self.change_day_title()

        # Add slot connector.
        self.d.accepted.connect(self.on_dialog_agenda_accepted)
        self.day_selector.currentChanged.connect(self.on_day_selector_value_change)
        self.list_agenda.currentItemChanged.connect(self.on_current_item_changed)

    def change_day_title(self):
        the_day = StringValidator.LOCALE_DAY_OF_WEEK[self.cur_day_int]
        self.findChild(QtWidgets.QLabel, 'app_title').setText(f'Jadwal Sepekan: Hari {the_day}')

    @pyqtSlot()
    def on_btn_add_clicked(self):
        # Prompt for user input value.
        the_day = StringValidator.LOCALE_DAY_OF_WEEK[self.cur_day_int]
        self.call_action('new', the_day)

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        if self.cur_item is None:
            return

        # The title of the currently selected item.
        title = self.cur_item.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data agenda.',
            f'Apakah Anda yakin akan menghapus agenda: {title} dari GKI Salatiga+?'
            f'\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # The old data.
            old_item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            old_day = old_item_data[0]
            old_name = old_item_data[1]
            old_time = old_item_data[2]
            old_place = old_item_data[3]
            old_representative = old_item_data[4]
            old_order = old_item_data[5]

            # Find the index of this item.
            idx = self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].index({
                'name': old_name,
                'time': old_time,
                'place': old_place,
                'representative': old_representative
            })

            # Now we find the new index order of this item.
            order = idx

            # Remove this item from the agenda dict.
            self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].__delitem__(order)

            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_agenda').indexFromItem(self.cur_item).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_agenda').takeItem(y_pos)

            # Logging.
            Lg('main.FrameAgenda.on_btn_delete_clicked', f'Removed the agenda info: {title} successfully!')
        else:
            Lg('main.FrameAgenda.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's data.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
        day = StringValidator.LOCALE_DAY_OF_WEEK[self.DAY_OF_WEEK_KEY.index(item_data[0])]
        name = item_data[1]
        time = item_data[2]
        place = item_data[3]
        representative = item_data[4]
        order = item_data[5]

        # Prompt for user input value.
        self.call_action('edit', day, name, time, place, representative, order)

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Overwrite the existing forms object.
        app_db.db['agenda'] = self.agenda_dict

        # Save to local file.
        app_db.save_local('agenda')

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    def on_current_item_changed(self):
        # Save the state of the currently selected item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_agenda').currentItem()

        # The QListWidgetItem object of the selected item.
        a = self.findChild(QtWidgets.QListWidget, 'list_agenda').currentItem()
        if a == None:
            return

        # The selected item's index.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_agenda').indexFromItem(a).row()

        # Change the non-user-editable field display.
        the_day = StringValidator.LOCALE_DAY_OF_WEEK[self.cur_day_int]
        self.findChild(QtWidgets.QLabel, 'label_day').setText(the_day)

        # Update the display data.
        item_data = self.findChild(QtWidgets.QListWidget, 'list_agenda').item(y_pos).data(self.DEFAULT_ITEM_ROLE)
        day_locale_text = StringValidator.LOCALE_DAY_OF_WEEK[self.DAY_OF_WEEK_KEY.index(item_data[0])]
        self.findChild(QtWidgets.QLabel, 'label_name').setText(item_data[1])
        self.findChild(QtWidgets.QLabel, 'label_day').setText(day_locale_text)
        self.findChild(QtWidgets.QLabel, 'label_time').setText(item_data[2] + ' WIB')
        self.findChild(QtWidgets.QLabel, 'label_place').setText(item_data[3])
        self.findChild(QtWidgets.QLabel, 'label_representative').setText(item_data[4])

    def on_day_selector_value_change(self):
        self.cur_day_int = self.findChild(QtWidgets.QTabWidget, 'day_selector').currentIndex()

        # Change the title appropriately.
        self.change_day_title()

        # Populate the QListWidget with the day's agenda.
        self.prefill_list_items()

    def on_dialog_agenda_accepted(self):
        # The input dialog's field data.
        name = self.d.findChild(QtWidgets.QLineEdit, 'field_name').text().strip()
        time = self.d.findChild(QtWidgets.QTimeEdit, 'event_time').time()
        place = self.d.findChild(QtWidgets.QLineEdit, 'field_place').text().strip()
        representative = self.d.findChild(QtWidgets.QLineEdit, 'field_representative').text().strip()

        # The "hidden" item order.
        order = int(self.d.findChild(QtWidgets.QLabel, 'app_title').toolTip())

        # Convert the time appropriately.
        time_h = self.zero_pad_time(time.hour())
        time_m = self.zero_pad_time(time.minute())
        time = time_h + ':' + time_m

        # The display title.
        display_text = f'{time} WIB --- {name}'

        if self.action == 'new':
            Lg('main.FrameAgenda.on_dialog_agenda_accepted', f'Creating a new agenda: {display_text} ...')

            # Append to the dict.
            self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].append({
                'name': name,
                'time': time,
                'place': place,
                'representative': representative
            })

            # Update the item's order.
            order = len(self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]]) - 1

            # Add a new item to the list.
            # Adding the list item.
            a = QtWidgets.QListWidgetItem()
            a.setData(
                self.DEFAULT_ITEM_ROLE,
                (self.DAY_OF_WEEK_KEY[self.cur_day_int], name, time, place, representative, order)
            )
            a.setText(display_text)
            self.findChild(QtWidgets.QListWidget, 'list_agenda').addItem(a)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_agenda').setCurrentItem(a)

        elif self.action == 'edit':
            Lg('main.FrameAgenda.on_dialog_agenda_accepted', f'Editing an existing agenda info: {display_text} ...')

            # The old data.
            old_item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            old_day = old_item_data[0]
            old_name = old_item_data[1]
            old_time = old_item_data[2]
            old_place = old_item_data[3]
            old_representative = old_item_data[4]
            old_order = old_item_data[5]

            # Find the index of this item.
            idx = self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].index({
                'name': old_name,
                'time': old_time,
                'place': old_place,
                'representative': old_representative
            })

            # Now we find the new index order of this item.
            order = idx

            # Edit the selected item's value.
            self.cur_item.setText(display_text)
            self.cur_item.setData(
                self.DEFAULT_ITEM_ROLE,
                (self.DAY_OF_WEEK_KEY[self.cur_day_int], name, time, place, representative, order)
            )

            # Now, edit the actual dict.
            self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]][order] = {
                'name': name,
                'time': time,
                'place': place,
                'representative': representative
            }

        # Update the current selection and state.
        self.on_current_item_changed()

    def prefill_list_items(self):
        """
        Populate the QListWidget with the agenda list found in the GKI Salatiga+ JSON data.
        :return: nothing.
        """
        # Remove any selection.
        self.findChild(QtWidgets.QListWidget, 'list_agenda').clearSelection()

        # Remove any existing or previous item in the QListWidget.
        self.findChild(QtWidgets.QListWidget, 'list_agenda').clear()

        # Iterating through every list of existing forms in the agenda dict.
        the_day_key = self.DAY_OF_WEEK_KEY[self.cur_day_int]
        for a in self.agenda_dict[the_day_key]:
            # The current agenda's order in the dict.
            item_order = self.agenda_dict[the_day_key].index(a)

            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(
                self.DEFAULT_ITEM_ROLE,
                (the_day_key, a['name'], a['time'], a['place'], a['representative'], item_order)
            )
            b.setText(f'{a['time']} WIB --- {a['name']}')
            self.findChild(QtWidgets.QListWidget, 'list_agenda').addItem(b)

        # Sort the list alphanumerically. [13]
        self.findChild(QtWidgets.QListWidget, 'list_agenda').setSortingEnabled(True)

    def zero_pad_time(self, time_int: int):
        if time_int < 10:
            return f'0{time_int}'
        else:
            return str(time_int)

    def call_action(self, action,
                    day: str = '',
                    name: str = '',
                    time: str = '',
                    place: str = '',
                    representative: str = '',
                    order: int = -1):
        """
        Determine what agenda action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the agenda action to undergo.
        :param name: (optional) the current agenda's name.
        :param day: (optional) the current agenda's day.
        :param time: (optional) the current agenda's time.
        :param place: (optional) the current agenda's place.
        :param representative: (optional) the current agenda's representative.
        :param order: (optional) the current agenda's index in the agenda dict.
        :return: nothing.
        """
        self.action = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Agenda Mingguan Baru')

            # Clear the existing title and URL.
            self.d.findChild(QtWidgets.QLineEdit, 'field_name').setText('')
            self.d.findChild(QtWidgets.QLabel, 'field_day').setText(day)
            self.d.findChild(QtWidgets.QLineEdit, 'field_place').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_representative').setText('')
            self.d.findChild(QtWidgets.QTimeEdit, 'event_time').setTime(QTime(0, 0, 0, 0))

            # We store the index here.
            self.d.findChild(QtWidgets.QLabel, 'app_title').setToolTip(str(order))

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Agenda Mingguan')

            # Preform the time to a QTime object.
            the_time_str = time.split(':')
            the_time = QTime(int(the_time_str[0]), int(the_time_str[1]), 0, 0)

            # Prefill with existing values.
            self.d.findChild(QtWidgets.QLineEdit, 'field_name').setText(name)
            self.d.findChild(QtWidgets.QLabel, 'field_day').setText(day)
            self.d.findChild(QtWidgets.QLineEdit, 'field_place').setText(place)
            self.d.findChild(QtWidgets.QLineEdit, 'field_representative').setText(representative)
            self.d.findChild(QtWidgets.QTimeEdit, 'event_time').setTime(the_time)

            # We store the index here.
            self.d.findChild(QtWidgets.QLabel, 'app_title').setToolTip(str(order))

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_fields()


class FrameCarousel(QtWidgets.QFrame, frame_carousel.Ui_Frame):

    # Some type constants.
    CAROUSEL_TYPE_POSTER = 'poster'
    CAROUSEL_TYPE_YOUTUBE = 'yt'
    CAROUSEL_TYPE_URL = 'article'

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    def __init__(self, *args, obj=None, **kwargs):
        super(FrameCarousel, self).__init__(*args, **kwargs)
        self.action = None
        self.cur_item = None
        self.setupUi(self)

        # Initiating the prompt and viewer dialogs.
        self.c = DialogCarousel(self)
        self.p = DialogPoster(self)

        # Initiate inital values according to the original, non-edited JSON schema.
        self.carousel_dict = copy.deepcopy(app_db.db['carousel'])

        # Initialize the initial values.
        self.prefill_list_items()

        # Add slot connector.
        self.c.accepted.connect(self.on_dialog_carousel_accepted)
        self.list_carousel.currentItemChanged.connect(self.on_current_item_changed)

    def call_action(self, action):
        """
        Determine what carousel action to take, as well as displaying the dialog.
        Possible values: 'new', 'edit', and 'poster' (i.e., poster viewer).
        :param action: specifies the agenda action to undergo.
        :return: nothing.
        """
        # Only call actions if there is some item selected.
        if self.cur_item is None and action != 'new':
            return
        else:
            self.action = action

        # Only applies to non-new actions.
        if action != 'new':
            # The selected item's key string and data.
            carousel_key = self.cur_item.data(self.DEFAULT_ITEM_ROLE)[0]
            carousel_dict = self.cur_item.data(self.DEFAULT_ITEM_ROLE)[1]

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.c.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Komedi Putar GKI Salatiga+ Baru')
            self.c.set_action(action)

            # Displaying the combo box carousel type.
            self.c.findChild(QtWidgets.QComboBox, 'carousel_type').setEnabled(True)

            # Displaying the editor fragment.
            if self.c.cur_idx >= 0:
                self.c.clear_fragment_and_display(self.c.CONST_CAROUSEL_FRAGMENT_INT[self.c.cur_idx])

            # Prefill with preliminary data.
            self.c.prefill_fragment_elements()

        elif action == 'edit':
            self.c.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Komedi Putar GKI Salatiga+')
            self.c.set_action(action)

            # Fill the edit data.
            self.c.populate_edit_data(carousel_key, carousel_dict)

            # The carousel type as well as the type's associated combo box index.
            type_idx = -1
            if carousel_dict['type'] == self.CAROUSEL_TYPE_POSTER:
                type_idx = 0
            elif carousel_dict['type'] == self.CAROUSEL_TYPE_YOUTUBE:
                type_idx = 1
            elif carousel_dict['type'] == self.CAROUSEL_TYPE_URL:
                type_idx = 2

            # DEBUG.
            # print('TYPE_IDX: ', type_idx)

            # Displaying the editor fragment.
            if type_idx >= 0:
                self.c.clear_fragment_and_display(self.c.CONST_CAROUSEL_FRAGMENT_INT[type_idx])

            # Displaying the combo box carousel type.
            self.c.findChild(QtWidgets.QComboBox, 'carousel_type').setEnabled(False)
            self.c.findChild(QtWidgets.QComboBox, 'carousel_type').setCurrentIndex(type_idx)

            # Prefill the data to edit.
            self.c.prefill_fragment_elements()

        elif action == 'poster' and carousel_dict['type'] == self.CAROUSEL_TYPE_POSTER:
            self.p.findChild(QtWidgets.QLabel, 'app_title').setText(carousel_dict['title'])
            self.p.findChild(QtWidgets.QLabel, 'app_caption').setText(carousel_dict['poster-caption'])

            # Displaying the pixmap.
            pixmap_loc = app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + carousel_key + os.sep + carousel_dict['poster-image']
            pixmap = QPixmap(pixmap_loc)
            self.p.findChild(QtWidgets.QLabel, 'poster_viewer').setPixmap(pixmap)

        # Show the dialog.
        if action == 'new' or action == 'edit':
            self.c.show()
        elif action == 'poster':
            self.p.show()


    @pyqtSlot()
    def on_btn_add_clicked(self):
        # Prompt for user input value.
        self.call_action('new')

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        if self.cur_item is None:
            return

        # We need at least one banner to go.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_carousel').__len__()
        if widget_size <= 1:
            QtWidgets.QMessageBox.warning(
                self, 'Tidak dapat menghapus item.',
                f'Harus ada minimal satu item pada komedi putar GKI Salatiga+!'
            )
            return

        # The title of the currently selected item.
        title = self.cur_item.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data agenda.',
            f'Apakah Anda yakin akan menghapus: {title} dari GKI Salatiga+?'
            f'\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # The old data.
            old_item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            old_key = old_item_data[0]
            old_data = old_item_data[1]

            # Remove this item from the agenda dict.
            self.carousel_dict.__delitem__(old_key)

            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_carousel').indexFromItem(self.cur_item).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_carousel').takeItem(y_pos)

            # Logging.
            Lg('main.FrameCarousel.on_btn_delete_clicked', f'Removed: {title} successfully!')
        else:
            Lg('main.FrameCarousel.on_btn_delete_clicked', f'Phew! It did not get removed.')

        # DEBUG.
        # print(self.carousel_dict)

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        # Prompt for user input value.
        self.call_action('edit')

    @pyqtSlot()
    def on_btn_move_down_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_carousel').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_carousel').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_carousel').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_carousel').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_carousel').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_move_up_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_carousel').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_carousel').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_carousel').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_carousel').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_poster_clicked(self):
        # Prompt for user input value.
        self.call_action('poster')

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Creating the JSON array to replace the old one.
        a = {}

        # Iterating through every item.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_carousel').__len__()):
            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_carousel').item(i)
            c = b.data(self.DEFAULT_ITEM_ROLE)

            # The item key and dict data.
            key = c[0]
            data = c[1]

            # Add this item to the JSON dict.
            a[key] = data

        # Overwrite the existing forms object.
        app_db.db['carousel'] = a

        # Save to local file.
        app_db.save_local('carousel')

        # Trigger uploading/pushing of the carousel.
        app_assets.do_upload_carousel = True

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    def on_current_item_changed(self):
        # Save the state of the currently selected item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_carousel').currentItem()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_carousel').__len__()

        # DEBUG.
        # print('WHY ERROR? ', self.cur_item, widget_size)

        # Skip empty list.
        if self.cur_item is None:
            return

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_carousel').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_carousel').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

        # Obtain the list item's hidden data.
        item_key = self.findChild(QtWidgets.QListWidget, 'list_carousel').item(y_pos).data(self.DEFAULT_ITEM_ROLE)[0]
        item_data = self.findChild(QtWidgets.QListWidget, 'list_carousel').item(y_pos).data(self.DEFAULT_ITEM_ROLE)[1]

        # Determine the item type.
        item_type = ''
        if item_data['type'] == self.CAROUSEL_TYPE_URL:
            item_type = 'Artikel Web'
        elif item_data['type'] == self.CAROUSEL_TYPE_YOUTUBE:
            item_type = 'Video YouTube'
        elif item_data['type'] == self.CAROUSEL_TYPE_POSTER:
            item_type = 'Gambar Poster'

        # Format the date.
        creation_date = StringValidator.get_full_date(item_data['date-created'])

        # Update the display data.
        self.findChild(QtWidgets.QLabel, 'label_name').setText(item_data['title'])
        self.findChild(QtWidgets.QLabel, 'label_type').setText(item_type)
        self.findChild(QtWidgets.QLabel, 'label_date').setText(creation_date)

        # Update the banner pixmap.
        pixmap_loc = app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + item_key + os.sep + item_data['banner']
        # Lg('main.FrameCarousel.on_current_item_changed', f'Displaying the carousel pixmap banner: {pixmap_loc}')
        pixmap = QPixmap(pixmap_loc)
        self.findChild(QtWidgets.QLabel, 'thumbnail_viewer').setPixmap(pixmap)

        # Clear the previous display.
        self.findChild(QtWidgets.QLabel, 'label_yt_val').setText('-')
        self.findChild(QtWidgets.QLabel, 'label_yt_val').setToolTip('')
        self.findChild(QtWidgets.QLabel, 'label_url_val').setText('-')
        self.findChild(QtWidgets.QLabel, 'label_url_val').setToolTip('')

        # Update the data type-specific information.
        if item_data['type'] == self.CAROUSEL_TYPE_URL:
            self.findChild(QtWidgets.QLabel, 'label_url_val').setText(item_data['article-url'])
            self.findChild(QtWidgets.QLabel, 'label_url_val').setToolTip(item_data['article-url'])
        elif item_data['type'] == self.CAROUSEL_TYPE_YOUTUBE:
            self.findChild(QtWidgets.QLabel, 'label_yt_val').setText(item_data['yt-link'])
            self.findChild(QtWidgets.QLabel, 'label_yt_val').setToolTip(item_data['yt-link'])
        elif item_data['type'] == self.CAROUSEL_TYPE_POSTER:
            pass

        # Enabling/disabling an element.
        self.findChild(QtWidgets.QLabel, 'label_yt_title').setEnabled(item_data['type'] == self.CAROUSEL_TYPE_YOUTUBE)
        self.findChild(QtWidgets.QLabel, 'label_yt_val').setEnabled(item_data['type'] == self.CAROUSEL_TYPE_YOUTUBE)
        self.findChild(QtWidgets.QLabel, 'label_url_title').setEnabled(item_data['type'] == self.CAROUSEL_TYPE_URL)
        self.findChild(QtWidgets.QLabel, 'label_url_val').setEnabled(item_data['type'] == self.CAROUSEL_TYPE_URL)
        self.findChild(QtWidgets.QLabel, 'label_poster').setEnabled(item_data['type'] == self.CAROUSEL_TYPE_POSTER)
        self.findChild(QtWidgets.QPushButton, 'btn_poster').setEnabled(item_data['type'] == self.CAROUSEL_TYPE_POSTER)

    def on_dialog_carousel_accepted(self):
        # The input dialog's field data.
        title = self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()

        # The display title.
        display_text = f'{title}'

        # Preparing the current item's data payload.
        item_type_idx = self.c.findChild(QtWidgets.QComboBox, 'carousel_type').currentIndex()
        item_type = self.c.CONST_CAROUSEL_TYPE_INT[item_type_idx]
        new_key = ('item_' + str(time.time_ns())) if self.action == 'new' else self.cur_item.data(self.DEFAULT_ITEM_ROLE)[0]
        new_data = {}

        # Creating this carousel item's base directory.
        base = app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + new_key
        os.makedirs(base, exist_ok=True)

        if item_type == self.CAROUSEL_TYPE_POSTER:

            # Duplicating the banner from local path to Simon Petrus' internal storage.
            banner_source = self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').toolTip().strip()
            banner_dest_filename = 'banner_' + str(time.time_ns()) + os.path.splitext(banner_source)[1]
            banner_dest = base + os.sep + banner_dest_filename

            # Copying the banner.
            # Using binary read, which is pretty cool
            with open(banner_source, 'rb') as fi:
                new_banner_bytes = fi.read()
            with open(banner_dest, 'wb') as fo:
                fo.write(new_banner_bytes)

            # Duplicating the poster from local path to Simon Petrus' internal storage.
            poster_source = self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_poster_loc').toolTip().strip()
            poster_dest_filename = 'poster_' + str(time.time_ns()) + os.path.splitext(poster_source)[1]
            poster_dest = base + os.sep + poster_dest_filename

            # Copying the poster.
            # Using binary read, which is pretty cool
            with open(poster_source, 'rb') as fi:
                new_poster_bytes = fi.read()
            with open(poster_dest, 'wb') as fo:
                fo.write(new_poster_bytes)

            new_data = {
                'banner': banner_dest_filename,
                'title': self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').text().strip(),
                'type': item_type,
                'date-created': self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_date').toolTip().strip(),
                'poster-image': poster_dest_filename,
                'poster-caption': self.c.cur_frame_obj.findChild(QtWidgets.QPlainTextEdit,
                                                                 'txt_caption').toPlainText().strip()
            }

        elif item_type == self.CAROUSEL_TYPE_YOUTUBE:

            # The YouTube video thumbnail.
            thumb = self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_yt_thumb').text().strip()

            # Downloading the YouTube thumbnail image.
            # Saving/downloading.
            download_url = thumb
            saved_dest_filename = 'banner_' + str(time.time_ns()) + os.path.splitext(thumb)[1]
            saved_dest = base + os.sep + saved_dest_filename
            urllib.request.urlretrieve(download_url, saved_dest)

            new_data = {
                'banner': saved_dest_filename,
                'title': self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').text().strip(),
                'type': item_type,
                'date-created': self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_date').toolTip().strip(),
                'yt-title': self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_yt_title').text().strip(),
                'yt-date': self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_yt_date').toolTip().strip(),
                'yt-desc': self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_yt_desc').text().strip(),
                'yt-link': self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_url').text().strip(),
                'yt-thumbnail': thumb,
                'yt-is_live': int(
                    self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_yt_live').toolTip().strip())
            }

        elif item_type == self.CAROUSEL_TYPE_URL:

            # Duplicating the banner from local path to Simon Petrus' internal storage.
            banner_source = self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').toolTip().strip()
            banner_dest_filename = 'banner_' + str(time.time_ns()) + os.path.splitext(banner_source)[1]
            banner_dest = base + os.sep + banner_dest_filename

            # Copying the banner.
            # Using binary read, which is pretty cool
            with open(banner_source, 'rb') as fi:
                new_banner_bytes = fi.read()
            with open(banner_dest, 'wb') as fo:
                fo.write(new_banner_bytes)

            new_data = {
                'banner': banner_dest_filename,
                'title': self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').text().strip(),
                'type': item_type,
                'date-created': self.c.cur_frame_obj.findChild(QtWidgets.QLabel, 'field_date').toolTip().strip(),
                'article-url': self.c.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()
            }

        if self.action == 'new':
            Lg('main.FrameCarousel.on_dialog_carousel_accepted',
               f'Creating a new carousel: {display_text} with carousel key: {new_key} ...')

            # Append to the dict.
            self.carousel_dict[new_key] = new_data

            # Add a new item to the list.
            a = QtWidgets.QListWidgetItem()
            a.setData(self.DEFAULT_ITEM_ROLE,(new_key, new_data))
            a.setText(display_text)
            self.findChild(QtWidgets.QListWidget, 'list_carousel').addItem(a)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_carousel').setCurrentItem(a)

        elif self.action == 'edit':
            Lg('main.FrameCarousel.on_dialog_carousel_accepted', f'Editing an existing carousel info: {display_text} ...')

            # The old data.
            old_item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            old_key = old_item_data[0]
            old_data = old_item_data[1]

            # Change the old data.
            self.carousel_dict[old_key] = new_data

            # Edit the selected item's value.
            self.cur_item.setText(display_text)
            self.cur_item.setData(self.DEFAULT_ITEM_ROLE, (new_key, new_data))

        # DEBUG.
        # print('NEW: ', new_key, new_data)
        # print('-' * 20)
        # print('DICT: ', self.carousel_dict)

        # Update the current selection and state.
        self.on_current_item_changed()

    def prefill_list_items(self):
        """
        Populate the QListWidget with the carousel list found in the GKI Salatiga+ JSON data.
        :return: nothing.
        """
        # Remove any selection.
        self.findChild(QtWidgets.QListWidget, 'list_carousel').clearSelection()

        # Remove any existing or previous item in the QListWidget.
        self.findChild(QtWidgets.QListWidget, 'list_carousel').clear()

        # Iterating through every list of existing forms in the carousel dict.
        for a in self.carousel_dict.keys():
            # The dict data of the current key.
            cur_data = self.carousel_dict[a]

            # The default value.
            item_data = ()

            # Determines the carousel type to determine which data to load.
            '''if cur_data['type'] == self.CAROUSEL_TYPE_URL:
                item_data = (cur_data['banner'], cur_data['title'], cur_data['type'], cur_data['date-created'],
                             cur_data['article-url'])
            elif cur_data['type'] == self.CAROUSEL_TYPE_POSTER:
                item_data = (cur_data['banner'], cur_data['title'], cur_data['type'], cur_data['date-created'],
                             cur_data['poster-image'], cur_data['poster-caption'])
            elif cur_data['type'] == self.CAROUSEL_TYPE_YOUTUBE:
                item_data = (cur_data['banner'], cur_data['title'], cur_data['type'], cur_data['date-created'],
                             cur_data['yt-title'], cur_data['yt-date'], cur_data['yt-desc'], cur_data['yt-link'],
                             cur_data['yt-thumbnail'], cur_data['yt-is_live'])'''

            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            # b.setData(self.DEFAULT_ITEM_ROLE, item_data)
            b.setData(self.DEFAULT_ITEM_ROLE, (a, cur_data))
            b.setText(cur_data['title'])
            self.findChild(QtWidgets.QListWidget, 'list_carousel').addItem(b)

        # Sort the list alphanumerically. [13]
        self.findChild(QtWidgets.QListWidget, 'list_carousel')


class FrameCarouselArticle(QtWidgets.QFrame, frame_carousel_article.Ui_FrameArticle):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameCarouselArticle, self).__init__(*args, **kwargs)
        self.img_mime_valid = None
        self.img_loc = None
        self.parent_button_box = None
        self.setupUi(self)
        self.b = DialogBanner(self)

        # Connect the slots.
        self.field_title.textChanged.connect(self.validate_fields)
        self.field_url.textChanged.connect(self.validate_fields)

    @pyqtSlot()
    def on_btn_img_select_clicked(self):
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih media dalam bentuk gambar untuk dijadikan banner komedi putar GKI Salatiga+', '', ff)[0]

        # Display the currently selected image file for uploading.
        if not loc == '':
            self.img_loc = loc
            img_basename = os.path.basename(self.img_loc)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(img_basename)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(loc)

            # Validate all inputs in general.
            self.validate_fields()

    @pyqtSlot()
    def on_btn_img_view_clicked(self):
        # Set the banner title.
        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text()
        self.b.findChild(QtWidgets.QLabel, 'app_title').setText(title)

        # Set the banner pixmap.
        pixmap_loc = self.findChild(QtWidgets.QLabel, 'txt_img_loc').toolTip()
        pixmap = QPixmap(pixmap_loc)
        self.b.findChild(QtWidgets.QLabel, 'banner_viewer').setPixmap(pixmap)

        # Show the dialog window.
        self.b.show()

    def set_parent_button_box(self, parent_button_box: QtWidgets.QDialogButtonBox):
        self.parent_button_box = parent_button_box

    def validate_fields(self):
        parent_button_box = self.parent_button_box

        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()
        img_loc = self.findChild(QtWidgets.QLabel, 'txt_img_loc').toolTip().strip()

        # Validating the mimetype.
        # Finding the selected file's mime type. [14]
        if img_loc != '':
            file_mimetype = Mgc(mime=True).from_file(img_loc)
            if not file_mimetype.startswith('image/'):
                self.img_mime_valid = False
            else:
                self.img_mime_valid = True

        if title == '' or url == '' or img_loc == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan semua input!')
            parent_button_box.buttons()[0].setEnabled(False)
        elif url == '' or not url.startswith('http') or not url.__contains__('://'):
            self.findChild(QtWidgets.QLabel, 'label_status').setText('URL harus dimulai dengan "http://" atau "https://"')
            parent_button_box.buttons()[0].setEnabled(False)
        elif not self.img_mime_valid:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Sepertinya berkas yang Anda pilih bukan gambar.')
            parent_button_box.buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            parent_button_box.buttons()[0].setEnabled(True)

        if img_loc == '':
            self.findChild(QtWidgets.QPushButton, 'btn_img_view').setEnabled(False)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_img_view').setEnabled(True)


class FrameCarouselPoster(QtWidgets.QFrame, frame_carousel_poster.Ui_FramePoster):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameCarouselPoster, self).__init__(*args, **kwargs)
        self.poster_loc = None
        self.poster_mime_valid = None
        self.img_loc = None
        self.img_mime_valid = None
        self.parent_button_box = None
        self.setupUi(self)
        self.b = DialogBanner(self)
        self.p = DialogPoster(self)

        # Connect the slots.
        self.field_title.textChanged.connect(self.validate_fields)
        self.txt_caption.textChanged.connect(self.validate_fields)

    @pyqtSlot()
    def on_btn_img_select_clicked(self):
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih media dalam bentuk gambar untuk dijadikan banner komedi putar GKI Salatiga+', '', ff)[0]

        # Display the currently selected image file for uploading.
        if not loc == '':
            self.img_loc = loc
            img_basename = os.path.basename(self.img_loc)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(img_basename)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(loc)

            # Validate all inputs in general.
            self.validate_fields()

    @pyqtSlot()
    def on_btn_img_view_clicked(self):
        # Set the banner title.
        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text()
        self.b.findChild(QtWidgets.QLabel, 'app_title').setText(title)

        # Set the banner pixmap.
        pixmap_loc = self.findChild(QtWidgets.QLabel, 'txt_img_loc').toolTip()
        pixmap = QPixmap(pixmap_loc)
        self.b.findChild(QtWidgets.QLabel, 'banner_viewer').setPixmap(pixmap)

        # Show the dialog window.
        self.b.show()

    @pyqtSlot()
    def on_btn_poster_select_clicked(self):
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih media dalam bentuk gambar untuk dijadikan poster komedi putar GKI Salatiga+', '', ff)[0]

        # Display the currently selected image file for uploading.
        if not loc == '':
            self.poster_loc = loc
            img_basename = os.path.basename(self.poster_loc)
            self.findChild(QtWidgets.QLabel, 'txt_poster_loc').setText(img_basename)
            self.findChild(QtWidgets.QLabel, 'txt_poster_loc').setToolTip(loc)

            # Validate all inputs in general.
            self.validate_fields()

    @pyqtSlot()
    def on_btn_poster_view_clicked(self):
        # Set the poster title.
        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text()
        self.p.findChild(QtWidgets.QLabel, 'app_title').setText(title)

        # Set the poster caption.
        caption = self.findChild(QtWidgets.QPlainTextEdit, 'txt_caption').toPlainText()
        self.p.findChild(QtWidgets.QLabel, 'app_caption').setText(caption)

        # Set the poster pixmap.
        pixmap_loc = self.findChild(QtWidgets.QLabel, 'txt_poster_loc').toolTip()
        pixmap = QPixmap(pixmap_loc)
        self.p.findChild(QtWidgets.QLabel, 'poster_viewer').setPixmap(pixmap)

        # Show the dialog window.
        self.p.show()

    def set_parent_button_box(self, parent_button_box: QtWidgets.QDialogButtonBox):
        self.parent_button_box = parent_button_box

    def validate_fields(self):
        parent_button_box = self.parent_button_box

        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        img_loc = self.findChild(QtWidgets.QLabel, 'txt_img_loc').toolTip().strip()
        poster_loc = self.findChild(QtWidgets.QLabel, 'txt_poster_loc').toolTip().strip()
        caption = self.findChild(QtWidgets.QPlainTextEdit, 'txt_caption').toPlainText().strip()

        # Validating the mimetype.
        # Finding the selected file's mime type. [14]
        if img_loc != '':
            file_mimetype = Mgc(mime=True).from_file(img_loc)
            if not file_mimetype.startswith('image/'):
                self.img_mime_valid = False
            else:
                self.img_mime_valid = True

        # Validating the mimetype.
        # Finding the selected file's mime type. [14]
        if poster_loc != '':
            file_mimetype = Mgc(mime=True).from_file(poster_loc)
            if not file_mimetype.startswith('image/'):
                self.poster_mime_valid = False
            else:
                self.poster_mime_valid = True

        if title == '' or img_loc == '' or poster_loc == '' or caption == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan semua input!')
            parent_button_box.buttons()[0].setEnabled(False)
        elif not self.img_mime_valid:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Sepertinya berkas yang Anda pilih untuk "banner" bukan gambar.')
            parent_button_box.buttons()[0].setEnabled(False)
        elif not self.poster_mime_valid:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Sepertinya berkas yang Anda pilih untuk "poster" bukan gambar.')
            parent_button_box.buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            parent_button_box.buttons()[0].setEnabled(True)

        if img_loc == '':
            self.findChild(QtWidgets.QPushButton, 'btn_img_view').setEnabled(False)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_img_view').setEnabled(True)

        if poster_loc == '':
            self.findChild(QtWidgets.QPushButton, 'btn_poster_view').setEnabled(False)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_poster_view').setEnabled(True)


class FrameCarouselYouTube(QtWidgets.QFrame, frame_carousel_yt.Ui_FrameYouTube):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameCarouselYouTube, self).__init__(*args, **kwargs)
        self.is_youtube_link_valid = None
        self.parent_button_box = None
        self.setupUi(self)

        # Connect the slots.
        self.field_title.textChanged.connect(self.validate_fields)
        self.field_url.textChanged.connect(self.validate_fields)

    @pyqtSlot()
    def on_btn_fetch_clicked(self):

        # Obtaining the video ID from the user input.
        url = self.findChild(QtWidgets.QLineEdit, 'field_url').text()
        v = StringValidator.get_youtube_id_from_link(url)

        # Begin updating the WordPress main page.
        uploader = Uploader(anim, prefs, app_db)

        # Using multithreading to prevent GUI freezing [9]
        t = ThreadWithResult(target=uploader.get_yt_video_data, args=(v,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                yt_video_data = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Check if the video is found on YouTube.
        if yt_video_data['pageInfo']['totalResults'] == 0:
            self.is_youtube_link_valid = False
            self.validate_fields()

        else:
            j_snippet = yt_video_data['items'][0]['snippet']

            # Determine if this video is a livestreaming.
            is_live = 0
            if j_snippet['liveBroadcastContent'] == 'live':
                is_live = 1

            # The user-friendly 'is live' text.
            yt_is_live = 'Live' if is_live == 1 else 'Pre-Recorded'

            # The non-user-friendly date.
            raw_date = j_snippet['publishedAt'].split('T')[0]

            # Filling in the text fields.
            self.findChild(QtWidgets.QLineEdit, 'field_yt_title').setText(j_snippet['title'])
            self.findChild(QtWidgets.QLineEdit, 'field_yt_date').setText(StringValidator.get_full_date(raw_date))
            self.findChild(QtWidgets.QLineEdit, 'field_yt_date').setToolTip(raw_date)
            self.findChild(QtWidgets.QLabel, 'field_yt_live').setToolTip(str(is_live))
            self.findChild(QtWidgets.QLabel, 'field_yt_live').setText(yt_is_live)
            self.findChild(QtWidgets.QLabel, 'field_yt_desc').setText(j_snippet['description'])

            # Mitigate "max res thumbnail not found".
            if j_snippet['thumbnails'].keys().__contains__('maxres'):
                self.findChild(QtWidgets.QLineEdit, 'field_yt_thumb').setText(j_snippet['thumbnails']['maxres']['url'])
            else:
                self.findChild(QtWidgets.QLineEdit, 'field_yt_thumb').setText(j_snippet['thumbnails']['default']['url'])

        # Validate the fields again.
        self.validate_fields()

    def set_parent_button_box(self, parent_button_box: QtWidgets.QDialogButtonBox):
        self.parent_button_box = parent_button_box

    def validate_fields(self):
        parent_button_box = self.parent_button_box

        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()
        yt_title = self.findChild(QtWidgets.QLineEdit, 'field_yt_title').text().strip()
        yt_date = self.findChild(QtWidgets.QLineEdit, 'field_yt_date').text().strip()
        yt_thumb = self.findChild(QtWidgets.QLineEdit, 'field_yt_thumb').text().strip()
        yt_desc = self.findChild(QtWidgets.QLabel, 'field_yt_desc').text().strip()

        # DEBUG.
        # print(yt_title, yt_date, yt_thumb, yt_desc)

        self.is_youtube_link_valid = True
        if url == '' or not url.startswith('http') or not url.__contains__('://') or not url.__contains__('youtu'):
            self.is_youtube_link_valid = False
            self.findChild(QtWidgets.QPushButton, 'btn_fetch').setEnabled(False)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_fetch').setEnabled(True)

        if title == '' or url == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan semua input!')
            parent_button_box.buttons()[0].setEnabled(False)

        elif yt_title == '' or yt_date == '' or yt_thumb == '' or yt_desc == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus menyegarkan metadata video YouTube!')
            parent_button_box.buttons()[0].setEnabled(False)

        elif not self.is_youtube_link_valid:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('URL video YouTube Anda tidak valid!')

        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            parent_button_box.buttons()[0].setEnabled(True)


class FrameDefault(QtWidgets.QFrame, frame_default.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameDefault, self).__init__(*args, **kwargs)
        self.setupUi(self)


class FrameFormulir(QtWidgets.QFrame, frame_formulir.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameFormulir, self).__init__(*args, **kwargs)
        self.action = ''
        self.cur_item = QtWidgets.QListWidgetItem()
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogForms(self)

        # Populating the forms list with existing forms.
        self.init_prefilled_forms()

        # Add slot connector.
        self.d.accepted.connect(self.on_dialog_forms_accepted)
        self.list_forms.currentItemChanged.connect(self.on_current_item_changed)

    def init_prefilled_forms(self):
        """
        Populate the QListWidget with the forms list found in the GKI Salatiga+ JSON data.
        :return: nothing.
        """
        # Iterating through every list of existing forms in the JSON schema.
        for a in app_db.db['forms']:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setText(a['title'])
            b.setToolTip(a['url'])
            self.findChild(QtWidgets.QListWidget, 'list_forms').addItem(b)

    @pyqtSlot()
    def on_btn_add_clicked(self):
        # Prompt for user input value.
        self.call_action('new')

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        if self.cur_item is None:
            return

        # The title of the currently selected item.
        title = self.cur_item.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data formulir.',
            f'Apakah Anda yakin akan menghapus formulir: {title}?\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(self.cur_item).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_forms').takeItem(y_pos)

            # Logging.
            Lg('main.FrameFormulir.on_btn_delete_clicked', f'Removed the form: {title} successfully!')
        else:
            Lg('main.FrameFormulir.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's title and url.
        title = self.cur_item.text()
        url = self.cur_item.toolTip()

        # Prompt for user input value.
        self.call_action('edit', title, url)

    @pyqtSlot()
    def on_btn_move_down_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_forms').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_forms').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_forms').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_forms').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_move_up_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_forms').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_forms').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_forms').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Creating the JSON array to replace the old one.
        a = []

        # Iterating through every item.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_forms').__len__()):

            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_forms').item(i)

            # The item title and URL.
            title = b.text()
            url = b.toolTip()

            # Add this item to the JSON array.
            a.append({
                'title': title,
                'url': url
            })

        # Overwrite the existing forms object.
        app_db.db['forms'] = a

        # Save to local file.
        app_db.save_local('forms')

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    def on_current_item_changed(self):
        # Save the state of the currently selected item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_forms').currentItem()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_forms').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_forms').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

    @pyqtSlot()
    def on_dialog_forms_accepted(self):
        # The input dialog's title and URL fields.
        title = self.d.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.d.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()

        if self.action == 'new':
            Lg('main.FrameFormulir.on_dialog_forms_accepted', f'Creating a new form: {title} ...')

            # Add a new item to the list.
            a = QtWidgets.QListWidgetItem()
            a.setText(title)
            a.setToolTip(url)
            self.findChild(QtWidgets.QListWidget, 'list_forms').addItem(a)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_forms').setCurrentItem(a)

        elif self.action == 'edit':
            Lg('main.FrameFormulir.on_dialog_forms_accepted', f'Editing an existing form: {title} ...')

            # Edit the selected item's value.
            self.cur_item.setText(title)
            self.cur_item.setToolTip(url)

        # Update the current selection and state.
        self.on_current_item_changed()

    def call_action(self, action, edit_title: str = '', edit_url: str = ''):
        """
        Determine what forms action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the forms action to undergo.
        :param edit_title: (optional) the current form's title to edit.
        :param edit_url: (optional) the current form's url to edit.
        :return: nothing.
        """
        self.action = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Formulir Baru')

            # Clear the existing title and URL.
            self.d.findChild(QtWidgets.QLineEdit, 'field_title').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_url').setText('')

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Formulir')

            # Prefill with existing values.
            self.d.findChild(QtWidgets.QLineEdit, 'field_title').setText(edit_title)
            self.d.findChild(QtWidgets.QLineEdit, 'field_url').setText(edit_url)

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_fields()


class FramePersembahan(QtWidgets.QFrame, frame_persembahan.Ui_Frame):

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    def __init__(self, *args, obj=None, **kwargs):
        super(FramePersembahan, self).__init__(*args, **kwargs)
        self.action = None
        self.cur_item = None
        self.new_qris_loc = None
        self.qris_loc = None
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogPersembahan(self)

        # Populating the forms list with existing forms.
        self.init_prefilled_banks()

        # Attempt to download the current QRIS image from GitHub, then display the QRIS' pixmap.
        self.init_qris()
        self.reload_qris_pixmap()

        # Add slot connector.
        self.d.accepted.connect(self.on_dialog_banks_accepted)
        self.list_banks.currentItemChanged.connect(self.on_current_item_changed)

    def init_prefilled_banks(self):
        """
        Populate the QListWidget with the bank list found in the GKI Salatiga+ JSON data.
        :return: nothing.
        """
        # Iterating through every list of existing forms in the JSON schema.
        for a in app_db.db['offertory']:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(
                self.DEFAULT_ITEM_ROLE,
                (a['bank-name'], a['bank-abbr'], a['bank-number'], a['account-holder'])
            )
            b.setText(f'{a['bank-abbr']} {a['bank-number']}')
            self.findChild(QtWidgets.QListWidget, 'list_banks').addItem(b)

    def init_qris(self):

        # Using multithreading to prevent GUI freezing [9]
        # (Supress downloading so that the image will not get downloaded on frame change.)
        t = ThreadWithResult(target=app_assets.get_main_qris, args=(True,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                qris_loc = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Save the main QRIS path and share it to every member of this class.
        self.qris_loc = qris_loc

    def on_current_item_changed(self):
        # Save the state of the currently selected item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_banks').currentItem()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_banks').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_banks').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

        # Update the display data.
        item_data = self.findChild(QtWidgets.QListWidget, 'list_banks').item(y_pos).data(self.DEFAULT_ITEM_ROLE)
        self.findChild(QtWidgets.QLabel, 'label_bank_name').setText(item_data[0])
        self.findChild(QtWidgets.QLabel, 'label_bank_abbr').setText(item_data[1])
        self.findChild(QtWidgets.QLabel, 'label_number').setText(item_data[2])
        self.findChild(QtWidgets.QLabel, 'label_holder').setText(item_data[3])

    @pyqtSlot()
    def on_btn_add_clicked(self):
        # Prompt for user input value.
        self.call_action('new')

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        if self.cur_item is None:
            return

        # The title of the currently selected item.
        title = self.cur_item.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data transfer bank.',
            f'Apakah Anda yakin akan menghapus transfer bank: {title} dari GKI Salatiga+?'
            f'\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(self.cur_item).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_banks').takeItem(y_pos)

            # Logging.
            Lg('main.FramePersembahan.on_btn_delete_clicked', f'Removed the bank info: {title} successfully!')
        else:
            Lg('main.FramePersembahan.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's data.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
        bank_name = item_data[0]
        bank_abbr = item_data[1]
        number = item_data[2].replace('.', '')
        holder = item_data[3]

        # Prompt for user input value.
        self.call_action('edit', bank_abbr, bank_name, number, holder)

    @pyqtSlot()
    def on_btn_export_clicked(self):
        # Ask the user wherein this image should be stored.
        # (Qt5 has built-in overwrite confirmation dialog.)
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        exported_qris = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save the current QRIS image to ...', '', ff)[0]

        if exported_qris == '':
            # Report user cancelled operation.
            QtWidgets.QMessageBox.information(
                self, 'Operation Cancelled!', 'The QRIS image does not get exported.',
                QtWidgets.QMessageBox.Ok
            )

        else:
            Lg('main.FramePersembahan.on_btn_export_clicked', 'Exporting the current QRIS image ...')

            # Read the current QRIS image file as bytes.
            qris_image_as_byte = None
            with open(self.qris_loc, 'rb') as fi:
                qris_image_as_byte = fi.read()

            # Save the file.
            with open(exported_qris, 'wb') as fo:
                fo.write(qris_image_as_byte)

            # Report successful writing.
            QtWidgets.QMessageBox.information(
                self, 'Success!', f'QRIS image has been exported to: {exported_qris}',
                QtWidgets.QMessageBox.Ok
            )

    @pyqtSlot()
    def on_btn_img_select_clicked(self):
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih media dalam bentuk gambar untuk menggantikan QRIS saat ini', '', ff)[0]

        # Display the currently selected image file for uploading.
        if not loc == '':
            self.new_qris_loc = loc
            img_basename = os.path.basename(loc)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(img_basename)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(loc)

            # Change the QRIS pixmap.
            pixmap = QPixmap(loc)
            self.findChild(QtWidgets.QLabel, 'label_pixmap').setPixmap(pixmap)

    @pyqtSlot()
    def on_btn_move_down_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_banks').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_banks').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_banks').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_banks').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_move_up_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_banks').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_banks').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_banks').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Creating the JSON array to replace the old one.
        a = []

        # Iterating through every item.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_banks').__len__()):

            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_banks').item(i)

            # The item title and URL.
            item_data = b.data(self.DEFAULT_ITEM_ROLE)
            bank_name = item_data[0]
            bank_abbr = item_data[1]
            number = item_data[2]
            holder = item_data[3]

            # Add this item to the JSON array.
            a.append({
                'bank-name': bank_name,
                'bank-abbr': bank_abbr,
                'bank-number': number,
                'account-holder': holder
            })

        # Overwrite the existing forms object.
        app_db.db['offertory'] = a

        # Save to local file.
        app_db.save_local('offertory')

        # Queue to overwrite the existing QRIS code image file.
        # Only call this expression if there is a newer file selected.
        if self.new_qris_loc is not None:
            app_assets.queue_main_qris_change(self.new_qris_loc)

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    def on_dialog_banks_accepted(self):
        # The input dialog's field data.
        bank_name = self.d.findChild(QtWidgets.QLineEdit, 'field_bank_name').text().strip()
        bank_abbr = self.d.findChild(QtWidgets.QLineEdit, 'field_bank_abbr').text().strip()
        number = self.d.findChild(QtWidgets.QLineEdit, 'field_number').text().strip()
        holder = self.d.findChild(QtWidgets.QLineEdit, 'field_holder').text().strip()

        # Visually and string-wise edit the field data to match standard. [11]
        bank_abbr = bank_abbr.upper()

        s = [w for w in number]
        s.insert(3, '.') if len(s) >= 3 else s
        s.insert(6, '.') if len(s) >= 6 else s
        s.insert(10, '.') if len(s) >= 10 else s
        number = ''.join(s)

        # The display title.
        display_text = f'{bank_abbr} {number}'

        if self.action == 'new':
            Lg('main.FramePersembahan.on_dialog_banks_accepted', f'Creating a new bank: {display_text} ...')

            # Add a new item to the list.
            # Adding the list item.
            a = QtWidgets.QListWidgetItem()
            a.setData(
                self.DEFAULT_ITEM_ROLE,
                (bank_name, bank_abbr, number, holder)
            )
            a.setText(display_text)
            self.findChild(QtWidgets.QListWidget, 'list_banks').addItem(a)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_banks').setCurrentItem(a)

        elif self.action == 'edit':
            Lg('main.FramePersembahan.on_dialog_forms_accepted', f'Editing an existing bank info: {display_text} ...')

            # Edit the selected item's value.
            self.cur_item.setText(display_text)
            self.cur_item.setData(
                self.DEFAULT_ITEM_ROLE,
                (bank_name, bank_abbr, number, holder)
            )

        # Update the current selection and state.
        self.on_current_item_changed()

    def reload_qris_pixmap(self):
        """ Reload the QRIS Pixmap in this frame's main display. [12] """
        if os.path.isfile(self.qris_loc) and cur_fragment == 'fragment_persembahan':
            Lg('main.FramePersembahan.reload_qris_pixmap', f'Displaying the QRIS image from path: {self.qris_loc} ...')
            pixmap = QPixmap(self.qris_loc)
            self.label_pixmap.setPixmap(pixmap)

    def call_action(self, action,
                    edit_bank_abbr: str = '',
                    edit_bank_name: str = '',
                    edit_number: str = '',
                    edit_holder: str = ''):
        """
        Determine what bank action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the bank action to undergo.
        :param edit_bank_abbr: (optional) the current bank's abbreviation to edit.
        :param edit_bank_name: (optional) the current bank's full name to edit.
        :param edit_number: (optional) the current bank's account number to edit.
        :param edit_holder: (optional) the current bank's account holder to edit.
        :return: nothing.
        """
        self.action = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Info Transfer Bank Baru')

            # Clear the existing title and URL.
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_abbr').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_name').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_number').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_holder').setText('')

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Info Transfer Bank')

            # Prefill with existing values.
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_abbr').setText(edit_bank_abbr)
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_name').setText(edit_bank_name)
            self.d.findChild(QtWidgets.QLineEdit, 'field_number').setText(edit_number)
            self.d.findChild(QtWidgets.QLineEdit, 'field_holder').setText(edit_holder)

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_fields()


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
        app_db.save_local('ykb')

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
        app_db.save_local('url-profile')

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

        # Connect the slots.
        self.date_picker.selectionChanged.connect(self.on_date_picker_selection_changed)

    @pyqtSlot()
    def on_date_picker_selection_changed(self):
        cur_date = self.findChild(QtWidgets.QCalendarWidget, 'date_picker').selectedDate()
        cur_date_int = [cur_date.day(), cur_date.month(), cur_date.year()]

        # Validate the current date string.
        cur_month_name = StringValidator.LOCALE_MONTH_NAME[cur_date_int[1] - 1]

        # Store the properly formated and localized date, which will become the post title.
        self.localized_date = f'{cur_date_int[0]} {cur_month_name} {cur_date_int[2]}'

    @pyqtSlot()
    def on_btn_pdf_select_clicked(self):
        ff = 'Portable Document Format (*.pdf)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih berkas PDF tata ibadah untuk diunggah', '', ff)[0]

        # Display the currently selected PDF file for uploading.
        if not loc == '':
            self.pdf_loc = loc
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
        uploader = Uploader(anim, prefs, app_db)

        # Open the animation window and disable all elements in this window, to prevent user input.
        anim.clear_and_show()
        global win_main
        disable_widget(win_main)

        # Using multithreading to prevent GUI freezing [9]
        t = ThreadWithResult(target=uploader.upload_liturgi, args=(self.pdf_loc, post_title,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                is_success, msg = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Closing the loading animation and re-enable the window.
        enable_widget(win_main)
        anim.hide()

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
        self.on_date_picker_selection_changed()
        self.date_picker.selectionChanged.connect(self.on_date_picker_selection_changed)

    @pyqtSlot()
    def on_date_picker_selection_changed(self):
        cur_date = self.findChild(QtWidgets.QCalendarWidget, 'date_picker').selectedDate()
        cur_date_int = [cur_date.day(), cur_date.month(), cur_date.year()]

        # Validate the current date string.
        cur_month_name = StringValidator.LOCALE_MONTH_NAME[cur_date_int[1] - 1]

        # Store the properly formated and localized date, which will become the post title.
        self.localized_date = f'{cur_date_int[0]} {cur_month_name} {cur_date_int[2]}'

    @pyqtSlot()
    def on_btn_pdf_select_clicked(self):
        ff = 'Portable Document Format (*.pdf)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih berkas PDF warta jemaat untuk diunggah', '', ff)[0]

        # Display the currently selected PDF file for uploading.
        if not loc == '':
            self.pdf_loc = loc
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
        uploader = Uploader(anim, prefs, app_db)

        # Open the animation window and disable all elements in this window, to prevent user input.
        anim.clear_and_show()
        global win_main
        disable_widget(win_main)

        # Using multithreading to prevent GUI freezing [9]
        t = ThreadWithResult(target=uploader.upload_warta, args=(self.pdf_loc, post_title,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                is_success, msg = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Closing the loading animation and re-enable the window.
        enable_widget(win_main)
        anim.hide()

        # Display the status information.
        # Display whatever status message returned from the decryption to the user.
        msg_title = 'Berhasil mengunggah warta jemaat!' if is_success else 'Gagal mengunggah warta jemaat!'
        self.findChild(QtWidgets.QLabel, 'label_status').setText(msg_title)
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMessageBox.warning(
            self, msg_title, msg,
            QtWidgets.QMessageBox.Ok
        )


class FrameWordPressHome(QtWidgets.QFrame, frame_wp_homepage.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameWordPressHome, self).__init__(*args, **kwargs)
        self.img_loc = None
        self.setupUi(self)

        # Connect the slots.
        self.check_autodetect_yt.stateChanged.connect(self.on_check_autodetect_yt_state_changed)
        self.check_autodetect_ig.stateChanged.connect(self.on_check_autodetect_ig_state_changed)

    @pyqtSlot()
    def on_btn_execute_clicked(self):

        # Display preamble status.
        self.findChild(QtWidgets.QLabel, 'label_status').setText("Memperbarui halaman utama WordPress GKISalatiga.org ...")
        QtCore.QCoreApplication.processEvents()

        # Begin updating the WordPress main page.
        uploader = Uploader(anim, prefs, app_db)

        # Determining the execution arguments.
        is_autofetch_youtube = self.findChild(QtWidgets.QCheckBox, 'check_autodetect_yt').isChecked()
        is_autofetch_instagram = self.findChild(QtWidgets.QCheckBox, 'check_autodetect_ig').isChecked()
        custom_youtube_link = self.findChild(QtWidgets.QLineEdit, 'field_yt_link').text()
        custom_poster_img_path = self.img_loc

        # Open the animation window and disable all elements in this window, to prevent user input.
        anim.clear_and_show()
        global win_main
        disable_widget(win_main)

        # Using multithreading to prevent GUI freezing [9]
        t = ThreadWithResult(target=uploader.update_wp_homepage, args=(is_autofetch_youtube, is_autofetch_instagram, custom_youtube_link, custom_poster_img_path,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                is_success, msg = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Closing the loading animation and re-enable the window.
        enable_widget(win_main)
        anim.hide()

        # Display the status information.
        # Display whatever status message returned from the decryption to the user.
        msg_title = 'Berhasil memperbarui laman utama WordPress!' if is_success else 'Gagal memperbarui laman utama!'
        self.findChild(QtWidgets.QLabel, 'label_status').setText(msg_title)
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMessageBox.warning(
            self, msg_title, msg,
            QtWidgets.QMessageBox.Ok
        )

    @pyqtSlot()
    def on_btn_img_select_clicked(self):
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih media dalam bentuk gambar untuk dijadikan poster depan GKISalatiga.org', '', ff)[0]

        # Display the currently selected image file for uploading.
        if not loc == '':
            self.img_loc = loc
            img_basename = os.path.basename(self.img_loc)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(img_basename)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(self.img_loc)

    @pyqtSlot()
    def on_check_autodetect_yt_state_changed(self):
        if self.findChild(QtWidgets.QCheckBox, 'check_autodetect_yt').isChecked():
            self.findChild(QtWidgets.QLineEdit, 'field_yt_link').setEnabled(False)
            self.findChild(QtWidgets.QLabel, 'label_yt_helper').setEnabled(False)
        else:
            self.findChild(QtWidgets.QLineEdit, 'field_yt_link').setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'label_yt_helper').setEnabled(True)

    @pyqtSlot()
    def on_check_autodetect_ig_state_changed(self):
        if self.findChild(QtWidgets.QCheckBox, 'check_autodetect_ig').isChecked():
            self.findChild(QtWidgets.QPushButton, 'btn_img_select').setEnabled(False)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setEnabled(False)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_img_select').setEnabled(True)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setEnabled(True)


class ScreenSettings(QtWidgets.QMainWindow, screen_settings.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenSettings, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Displaying the appropriate settings value in each field.
        self.chk_autosync.setChecked(True if prefs.settings['autosync_on_launch'] == 1 else False)

    @pyqtSlot()
    def on_btn_apply_clicked(self):
        # Saving the settings value.
        prefs.settings['autosync_on_launch'] = 1 if self.chk_autosync.isChecked() == True else 0

        # Writing config into file.
        prefs.save_config()

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


class ScreenTest(QtWidgets.QMainWindow, screen_test.Ui_MainWindow):
    """ Used during development to try out new features and debug app's code. """

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenTest, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Preamble logging.
        Lg('main.ScreenTest', '[DEBUG] Initiating the debug ScreenTest window ...')

        # Which test method to run?
        # (Uncomment the ones not needed.)
        # self.test_001()

    def test_001(self):
        """ Displaying image using QPixmap. [12] """
        pixmap = QPixmap('assets/test_image.png')
        self.label_test.setPixmap(pixmap)


if __name__ == '__main__':
    # Initiating QApplication.
    app = QtWidgets.QApplication(sys.argv)

    # Initiating the global windows
    global anim
    global cur_fragment
    global win_main

    # Init the loading window animator.
    anim = ScreenLoadingAnimation()

    # Determining the default fragment to show at startup.
    cur_fragment = 'fragment_default'

    # Establishing the main window.
    # win = ScreenTest()  # --- debug only. uncomment if not needed.
    win = ScreenCredentialDecrypt()
    win.show()

    # Actually exiting the app.
    exit_code = app.exec()

    # Performing post-operation procedures.
    prefs.shutdown()

    # Appropriately exiting the app.
    sys.exit(exit_code)
