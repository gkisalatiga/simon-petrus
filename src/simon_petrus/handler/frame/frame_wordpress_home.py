"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
import os

import global_schema
from lib.external.thread import ThreadWithResult
from lib.uploader import Uploader
from ui import frame_wp_homepage


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
        uploader = Uploader()

        # Determining the execution arguments.
        is_autofetch_youtube = self.findChild(QtWidgets.QCheckBox, 'check_autodetect_yt').isChecked()
        is_autofetch_instagram = self.findChild(QtWidgets.QCheckBox, 'check_autodetect_ig').isChecked()
        custom_youtube_link = self.findChild(QtWidgets.QLineEdit, 'field_yt_link').text()
        custom_poster_img_path = self.img_loc

        # Open the animation window and disable all elements in this window, to prevent user input.
        global_schema.anim.clear_and_show()
        global_schema.disable_widget(global_schema.win_main)

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
        global_schema.enable_widget(global_schema.win_main)
        global_schema.anim.hide()

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
