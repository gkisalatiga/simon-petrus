"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from datetime import datetime as dt
import os

from handler.frame.frame_carousel_article import FrameCarouselArticle
from handler.frame.frame_carousel_poster import FrameCarouselPoster
from handler.frame.frame_carousel_youtube import FrameCarouselYouTube
from lib.string_validator import StringValidator
from ui import dialog_carousel
import global_schema


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
            banner_loc = global_schema.app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + self.carousel_key + os.sep + \
                         self.carousel_dict['banner']
            banner_loc_short = os.path.split(banner_loc)[1]
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(banner_loc_short)
            self.cur_frame_obj.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(banner_loc)

            # Set the poster location.
            poster_loc = global_schema.app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + self.carousel_key + os.sep + \
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
            banner_loc = global_schema.app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + self.carousel_key + os.sep + \
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
