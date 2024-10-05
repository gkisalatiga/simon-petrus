"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

import global_schema
from handler.dialog.dialog_changelog import DialogChangelog
from handler.dialog.dialog_license import DialogLicense
from handler.frame.frame_agenda import FrameAgenda
from handler.frame.frame_carousel import FrameCarousel
from handler.frame.frame_default import FrameDefault
from handler.frame.frame_formulir import FrameFormulir
from handler.frame.frame_gallery import FrameGallery
from handler.frame.frame_persembahan import FramePersembahan
from handler.frame.frame_playlist import FramePlaylist
from handler.frame.frame_renungan import FrameRenungan
from handler.frame.frame_social_media import FrameSocialMedia
from handler.frame.frame_static import FrameStatic
from handler.frame.frame_tata_ibadah import FrameTataIbadah
from handler.frame.frame_warta_jemaat import FrameWartaJemaat
from handler.frame.frame_wordpress_home import FrameWordPressHome
from handler.screen.screen_settings import ScreenSettings
from lib.external.meipass import resource_path
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from ui import screen_main


class ScreenMain(QtWidgets.QMainWindow, screen_main.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenMain, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # DEBUG. Displaying the default first fragment to display.
        Lg('ScreenMain', f'Displaying the first/default fragment: {global_schema.cur_fragment}')

        # Display the logo.
        # SOURCE: https://www.pythonguis.com/faq/adding-images-to-pyqt5-applications
        pixmap = QPixmap(resource_path('assets/seasonal_logo.png'))
        self.label_logo.setPixmap(pixmap)
        self.label_logo.setScaledContents(True)
        # self.label_logo.resize(pixmap.width(), pixmap.height())

        # Displaying the default fragment.
        self.clear_fragment_and_display(global_schema.cur_fragment)

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
            'fragment_gallery': FrameGallery(),
            'fragment_persembahan': FramePersembahan(),
            'fragment_playlist': FramePlaylist(),
            'fragment_renungan': FrameRenungan(),
            'fragment_social_media': FrameSocialMedia(),
            'fragment_static': FrameStatic(),
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
    def on_action_changelog_triggered(self):
        DialogChangelog(self).show()

    @pyqtSlot()
    def on_action_exit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_action_license_triggered(self):
        DialogLicense(self).show()

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
            global_schema.anim.clear_and_show()
            global_schema.disable_widget(global_schema.win_main)

            # Using multithreading to prevent GUI freezing [9]
            t = ThreadWithResult(target=global_schema.push_all_data, args=())
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
            global_schema.enable_widget(global_schema.win_main)
            global_schema.anim.hide()

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
        global_schema.anim.clear_and_show()
        global_schema.disable_widget(global_schema.win_main)

        # Fake the progression.
        msg = 'Menyinkronisasi basis data JSON dan berkas aset dari repositori GitHub ...'
        global_schema.anim.set_prog_msg(50, msg)
        Lg('main.ScreenMain.on_btn_sync_clicked', msg)

        # Using multithreading to prevent GUI freezing [9]
        t = ThreadWithResult(target=global_schema.refresh_all_data, args=())
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                is_success, refresh_msg = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Closing the loading animation and re-enable the window.
        global_schema.enable_widget(global_schema.win_main)
        global_schema.anim.hide()

        if is_success:
            QtWidgets.QMessageBox.information(
                self, 'Berhasil menyinkronisasi!',
                f'Data JSON dari repositori utama GKI Salatiga+ berhasil dimuat: {refresh_msg}',
                QtWidgets.QMessageBox.Ok
            )

            # Load the latest downloaded JSON schema into the app.
            global_schema.app_db.load_json_schema()

            # Refresh the Qt widget of the currently active fragment.
            self.clear_fragment_and_display(global_schema.cur_fragment)

        else:
            QtWidgets.QMessageBox.warning(
                self, 'Gagal memperbarui data JSON dari repositori GitHub!', refresh_msg,
                QtWidgets.QMessageBox.Ok
            )

    @pyqtSlot()
    def on_cmd_agenda_clicked(self):
        global_schema.cur_fragment = 'fragment_agenda'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_carousel_clicked(self):
        global_schema.cur_fragment = 'fragment_carousel'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_formulir_clicked(self):
        global_schema.cur_fragment = 'fragment_formulir'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_gallery_clicked(self):
        global_schema.cur_fragment = 'fragment_gallery'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_liturgi_clicked(self):
        global_schema.cur_fragment = 'fragment_tata_ibadah'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_persembahan_clicked(self):
        global_schema.cur_fragment = 'fragment_persembahan'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_playlist_clicked(self):
        global_schema.cur_fragment = 'fragment_playlist'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_renungan_clicked(self):
        global_schema.cur_fragment = 'fragment_renungan'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_social_media_clicked(self):
        global_schema.cur_fragment = 'fragment_social_media'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_static_clicked(self):
        global_schema.cur_fragment = 'fragment_static'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_warta_clicked(self):
        global_schema.cur_fragment = 'fragment_warta_jemaat'
        self.clear_fragment_and_display(global_schema.cur_fragment)

    @pyqtSlot()
    def on_cmd_wp_home_clicked(self):
        global_schema.cur_fragment = 'fragment_wp_home'
        self.clear_fragment_and_display(global_schema.cur_fragment)
