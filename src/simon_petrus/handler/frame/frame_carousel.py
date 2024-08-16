"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from urllib import request
import copy
import os
import time
import urllib

import global_schema
from handler.dialog.dialog_carousel import DialogCarousel
from handler.dialog.dialog_poster import DialogPoster
from lib.logger import Logger as Lg
from lib.string_validator import StringValidator
from ui import frame_carousel


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
        self.carousel_dict = copy.deepcopy(global_schema.app_db.db['carousel'])

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
            pixmap_loc = global_schema.app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + carousel_key + os.sep + carousel_dict['poster-image']
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
        global_schema.app_db.db['carousel'] = a

        # Save to local file.
        global_schema.app_db.save_local('carousel')

        # Trigger uploading/pushing of the carousel.
        global_schema.app_assets.do_upload_carousel = True

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
        pixmap_loc = global_schema.app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + item_key + os.sep + item_data['banner']
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
        base = global_schema.app_assets.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + new_key
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
