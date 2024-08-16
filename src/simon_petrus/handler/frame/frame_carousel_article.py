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
from lib.mimetypes import MimeTypes
from ui import frame_carousel_article


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
            file_mimetype = MimeTypes.guess_mimetype(img_loc)
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
