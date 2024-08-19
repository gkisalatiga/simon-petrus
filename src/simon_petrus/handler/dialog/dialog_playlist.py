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
from handler.frame.frame_playlist_regular import FramePlaylistRegular
from handler.frame.frame_playlist_rss import FramePlaylistRSS
from lib.string_validator import StringValidator
from ui import dialog_playlist
import global_schema


class DialogPlaylist(QtWidgets.QDialog, dialog_playlist.Ui_Dialog):

    # Some type constants.
    PLAYLIST_TYPE_REGULAR = 'regular'
    PLAYLIST_TYPE_RSS = 'rss'

    # This associates "const_carousel_fragment_dictionary" with the respective int.
    CONST_PLAYLIST_FRAGMENT_INT = [
        'fragment_playlist_regular',
        'fragment_playlist_rss',
    ]

    # This associates JSON's type constants with the respective int.
    CONST_PLAYLIST_TYPE_INT = [
        'regular',
        'rss',
    ]

    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogPlaylist, self).__init__(*args, **kwargs)
        self.action = None
        self.playlist_dict = None
        self.playlist_key = None
        self.cur_frame_obj = QtWidgets.QFrame()
        self.cur_idx = 0
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Connecting action slots.
        self.playlist_type.currentIndexChanged.connect(self.on_playlist_type_index_changed)

    def clear_fragment_and_display(self, fragment_str: str):
        """
        This function clears the current fragment and replace it with a new one automatically.
        :param fragment_str: the target fragment to display, as defined in the local fragment dictionary.
        :return: nothing.
        """
        # Prevents freezing [5]
        QtCore.QCoreApplication.processEvents()

        # The fragment dictionary.
        const_carousel_fragment_dictionary = {
            'fragment_playlist_regular': FramePlaylistRegular(),
            'fragment_playlist_rss': FramePlaylistRSS()
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

        # Redundant update of fragment index number.
        # (May cause infinite recursion error.)
        # self.on_playlist_type_index_changed()

    def clear_fragment_layout_content(self):
        """
        This function removes every child element from the GridLayout that is used
        to display the fragments. [4]
        :return: nothing.
        """
        for i in range(self.fragment_layout.count()):
            item = self.fragment_layout.itemAt(i).widget()
            item.deleteLater()

    def on_playlist_type_index_changed(self):
        self.cur_idx = self.findChild(QtWidgets.QComboBox, 'playlist_type').currentIndex()

        # Displaying the right fragment.
        self.clear_fragment_and_display(self.CONST_PLAYLIST_FRAGMENT_INT[self.cur_idx])

        # Ensures we have the prefilled date when the action is "new".
        self.prefill_fragment_elements()

    def populate_edit_data(self, playlist_key, playlist_dict):
        """
        Populate the current "edit" dialog state with a given existing carousel's data.
        :param playlist_key: the associated carousel key string.
        :param playlist_dict: the associated carousel data.
        :return: nothing.
        """
        self.playlist_key = playlist_key
        self.playlist_dict = playlist_dict

    def prefill_fragment_elements(self):
        """
        Prefill the currently active fragment's essential data.
        Only applies to "edit" actions.
        :return: nothing.
        """
        if not self.action == 'edit':
            return

        # DEBUG.
        # print('OBJ NAME: ', self.cur_frame_obj.objectName())
        # print('CAROUSEL TYPE: ', self.carousel_dict['type'])

        # Set the title and date, which is the same in all frames.
        title = self.playlist_dict['title']
        self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').setText(title)

        if self.playlist_dict['type'] == self.PLAYLIST_TYPE_REGULAR:
            # Set the title.
            title = self.playlist_dict['title']
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').setText(title)

            # Set the playlist URL.
            url = StringValidator.get_youtube_playlist_link_from_id(self.playlist_dict['playlist-id'])
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_url').setText(url)

        elif self.playlist_dict['type'] == self.PLAYLIST_TYPE_RSS:
            # Set the title.
            title = self.playlist_dict['title']
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_title').setText(title)

            # Set the RSS keyword.
            keyword = self.playlist_dict['rss-title-keyword']
            self.cur_frame_obj.findChild(QtWidgets.QLineEdit, 'field_key').setText(keyword)

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
