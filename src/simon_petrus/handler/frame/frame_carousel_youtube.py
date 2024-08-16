"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

from lib.external.thread import ThreadWithResult
from lib.string_validator import StringValidator
from lib.uploader import Uploader
from ui import frame_carousel_yt


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
        uploader = Uploader()

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
