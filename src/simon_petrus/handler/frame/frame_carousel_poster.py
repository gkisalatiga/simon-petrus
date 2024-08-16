"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
import os

from handler.dialog.dialog_banner import DialogBanner
from handler.dialog.dialog_poster import DialogPoster
from lib.mimetypes import MimeTypes
from ui import frame_carousel_poster


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
            file_mimetype = MimeTypes.guess_mimetype(img_loc)
            if not file_mimetype.startswith('image/'):
                self.img_mime_valid = False
            else:
                self.img_mime_valid = True

        # Validating the mimetype.
        # Finding the selected file's mime type. [14]
        if poster_loc != '':
            file_mimetype = MimeTypes.guess_mimetype(poster_loc)
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
