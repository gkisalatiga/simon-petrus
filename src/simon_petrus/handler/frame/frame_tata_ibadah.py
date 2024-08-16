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
from lib.string_validator import StringValidator
from lib.uploader import Uploader
from ui import frame_liturgi_upload


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
        uploader = Uploader()

        # Open the animation window and disable all elements in this window, to prevent user input.
        global_schema.anim.clear_and_show()
        global_schema.disable_widget(global_schema.win_main)

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
        global_schema.enable_widget(global_schema.win_main)
        global_schema.anim.hide()

        # Display the status information.
        # Display whatever status message returned from the decryption to the user.
        msg_title = 'Berhasil mengunggah tata ibadah!' if is_success else 'Gagal mengunggah tata ibadah!'
        self.findChild(QtWidgets.QLabel, 'label_status').setText(msg_title)
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMessageBox.warning(
            self, msg_title, msg,
            QtWidgets.QMessageBox.Ok
        )
