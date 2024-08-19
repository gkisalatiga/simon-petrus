"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from urllib.parse import urlparse
import copy
import pyperclip

import global_schema
from handler.dialog.dialog_playlist import DialogPlaylist
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from lib.string_validator import StringValidator
from lib.uploader import Uploader
from ui import frame_playlist


class FramePlaylist(QtWidgets.QFrame, frame_playlist.Ui_Frame):

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    # Converts fragment navigator string to JSON node name.
    PLAYLIST_NODE_DICT = {
        'list_pinned': 'pinned',
        'list_standard': 'standard'
    }

    def __init__(self, *args, obj=None, **kwargs):
        super(FramePlaylist, self).__init__(*args, **kwargs)
        self.active_list = 'list_standard'
        self.action = None
        self.cur_item = None
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogPlaylist(self)

        # Copy all things in the original dict.
        self.playlist_dict = copy.deepcopy(global_schema.app_db.db['yt'])

        # Prefill with information.
        self.prefill_fields()

        # Connect the slots.
        self.d.accepted.connect(self.on_dialog_forms_accepted)
        # self.combo_year.currentIndexChanged.connect(self.on_combo_year_index_changed)
        self.list_pinned.currentItemChanged.connect(self.on_list_pinned_item_changed)
        self.list_standard.currentItemChanged.connect(self.on_list_standard_item_changed)

    def call_action(self, action, kind: str = '', title: str = '', arg: str = ''):
        """
        Determine what playlist action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the gallery action to undergo.
        :param kind: (optional) the type of the current playlist.
        :param title: (optional) the current playlist title.
        :param arg: (optional) the additional argument for the current playlist.
        :return: nothing.
        """
        self.action = action
        self.d.set_action(action)

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Daftar Putar Baru')

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Daftar Putar')

            # Populate with the data
            cur_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            self.d.populate_edit_data(-1, cur_data)

            # Setting which fragment to display.
            kind = cur_data['type']
            self.d.cur_idx = self.d.CONST_PLAYLIST_TYPE_INT.index(kind)

        # Displaying the editor fragment.
        if self.d.cur_idx >= 0:
            self.d.clear_fragment_and_display(self.d.CONST_PLAYLIST_FRAGMENT_INT[self.d.cur_idx])

        # Prefill the data to edit.
        self.d.prefill_fragment_elements()

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_child_fragment()

    @pyqtSlot()
    def on_btn_add_clicked(self):
        # Prompt for user input value.
        self.call_action('new')

    @pyqtSlot()
    def on_btn_copy_gdrive_clicked(self):
        gdrive_url = self.findChild(QtWidgets.QLabel, 'label_url').toolTip()
        pyperclip.copy(gdrive_url)

        # Notify the user about successful copy.
        delete = QtWidgets.QMessageBox.information(
            self, 'Berhasil menyalin teks', f'Berhasil menyalin tautan folder Google Drive: {gdrive_url}',
            QtWidgets.QMessageBox.Ok
        )

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        if self.cur_item is None:
            return

        # The active list's JSON node name.
        active_node = self.PLAYLIST_NODE_DICT[self.active_list]

        # The title of the currently selected item.
        title = self.cur_item.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data folder galeri.',
            f'Apakah Anda yakin akan menghapus folder: {title}?\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, self.active_list).indexFromItem(self.cur_item).row()

            # The selected item's data in the gallery dict.
            item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)

            # Remove from the class' gallery dict.
            self.playlist_dict[active_node].remove(item_data)

            # Remove also the selected item from the list.
            self.findChild(QtWidgets.QListWidget, self.active_list).takeItem(y_pos)

            # Logging.
            Lg('main.FramePlaylist.on_btn_delete_clicked', f'Removed the playlist: {title} successfully!')
        else:
            Lg('main.FramePlaylist.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's inherent data.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)

        # The selected item's title and type.
        title = item_data['title']
        kind = item_data['type']

        # Filtering.
        if kind == 'rss':
            arg = item_data['rss-title-keyword']
        elif kind == 'regular':
            arg = item_data['playlist-id']

        # Prompt for user input value.
        self.call_action('edit', kind, title, arg)

    @pyqtSlot()
    def on_btn_fetch_clicked(self):
        # The currently selected item's Google Drive folder ID.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
        title = item_data['title']
        kind = item_data['type']

        # Disable all elements in this window, to prevent user input.
        global_schema.disable_widget(global_schema.win_main)
        global_schema.anim.clear_and_show()

        # The uploader object.
        uploader = Uploader()

        # Determining the right action to take.
        if kind == 'rss':
            f = item_data['rss-title-keyword']
            target=uploader.get_yt_rss_data
        elif kind == 'regular':
            target = uploader.get_yt_playlist_data
            f = item_data['playlist-id']

        # Using multithreading to prevent GUI freezing [9]
        # (Supress downloading so that the image will not get downloaded on frame change.)
        t = ThreadWithResult(target=target, args=(f,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                results = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Set last update value.
        item_data['last-update'] = StringValidator.get_date()

        # Apply the retrieved data to the currently selected item.
        a = []
        if kind == 'rss':
            for b in results:
                if not b['is_data_empty'] == 1:
                    a.append({
                        'title': b['video_title'],
                        'date': b['date_published'].split('T')[0],
                        'desc': b['video_description'],
                        'link': b['video_url'],
                        'thumbnail': b['video_thumbnail']
                    })
        elif kind == 'regular':
            for b in results['items']:

                # Mitigate "high quality" thumbnail cannot be specified.
                # (Or, if the video is private or already deleted.)
                if b['snippet']['thumbnails'] == {} or b['snippet']['title'] == 'Deleted video':
                    Lg('FramePlaylist', f'We cannot retrieve this iteration\'s video info: it is probably deleted.')
                    continue

                a.append({
                    'title': b['snippet']['title'],
                    'date': b['snippet']['publishedAt'].split('T')[0],
                    'desc': b['snippet']['description'],
                    'link': StringValidator.get_youtube_link_from_id(b['id']),
                    'thumbnail': b['snippet']['thumbnails']['high']['url']
                })

        # Overwriting the item's data.
        item_data['content'] = copy.deepcopy(a)
        self.cur_item.setData(self.DEFAULT_ITEM_ROLE, item_data)

        # Re-enable all elements in this window.
        global_schema.enable_widget(global_schema.win_main)
        global_schema.anim.hide()

        # Recalculate items and displays.
        self.on_list_pinned_item_changed()
        self.reconsider_playlist_order()

        # Notify the user about successful fetching.
        QtWidgets.QMessageBox.information(
            self, 'Berhasil memutakhirkan data!', f'Berhasil memutakhirkan data isi konten dari daftar putar: {title}',
            QtWidgets.QMessageBox.Ok
        )

        # Update the snippet display.
        self.update_snippet_data()

    @pyqtSlot()
    def on_btn_move_down_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, self.active_list).__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, self.active_list).indexFromItem(self.cur_item).row()

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, self.active_list).takeItem(y_pos)

        # Do not move down if already at the bottom.
        if y_pos == widget_size - 1:
            if self.active_list == 'list_pinned':
                # Move down the item to a different list.
                target_pos = 0
                self.findChild(QtWidgets.QListWidget, 'list_standard').insertItem(target_pos, a)
                self.findChild(QtWidgets.QListWidget, 'list_standard').setCurrentRow(target_pos)
            else:
                return

        else:
            # Move down the item within the same item list.
            target_pos = y_pos + 1
            self.findChild(QtWidgets.QListWidget, self.active_list).insertItem(target_pos, a)
            self.findChild(QtWidgets.QListWidget, self.active_list).setCurrentRow(target_pos)

        # Finally, reconsider JSON data order.
        self.reconsider_playlist_order()

    @pyqtSlot()
    def on_btn_move_up_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, self.active_list).indexFromItem(self.cur_item).row()

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, self.active_list).takeItem(y_pos)

        # Do not move up if already at the top.
        if y_pos == 0:
            if self.active_list == 'list_standard':
                # Move up the item to a different list.
                target_list_size = self.findChild(QtWidgets.QListWidget, 'list_pinned').__len__()
                target_pos = target_list_size
                self.findChild(QtWidgets.QListWidget, 'list_pinned').insertItem(target_pos, a)
                self.findChild(QtWidgets.QListWidget, 'list_pinned').setCurrentRow(target_pos)
            else:
                return

        else:
            # Move up the item within the same list.
            target_pos = y_pos - 1
            self.findChild(QtWidgets.QListWidget, self.active_list).insertItem(target_pos, a)
            self.findChild(QtWidgets.QListWidget, self.active_list).setCurrentRow(target_pos)

        # Finally, reconsider JSON data order.
        self.reconsider_playlist_order()

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Overwrite the existing forms object.
        global_schema.app_db.db['yt'] = copy.deepcopy(self.playlist_dict)

        # DEBUG.
        # print(self.playlist_dict)
        # print('=' * 25)
        # print(global_schema.app_db.db['yt'])

        # Save to local file.
        global_schema.app_db.save_local('yt')

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    @pyqtSlot()
    def on_combo_year_index_changed(self):
        # The selected year.
        year = self.findChild(QtWidgets.QComboBox, 'combo_year').currentText()

        if year == '':
            return

        # Remove the item list current selection.
        self.findChild(QtWidgets.QListWidget, 'list_gallery').setCurrentRow(-1)

        # Remove previous items to avoid duplication.
        self.findChild(QtWidgets.QListWidget, 'list_gallery').clear()

        # Iterate through every item in this year.
        for a in self.playlist_dict[year]:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(a['title'])
            self.findChild(QtWidgets.QListWidget, 'list_gallery').addItem(b)

    @pyqtSlot()
    def on_dialog_forms_accepted(self):
        # Creating a new JSON data.
        a = {
            'content': [],
            'last-update': StringValidator.get_date()
        }

        # The input dialog's title, URL, and story fields.
        title = self.d.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        a['title'] = title

        # Filtering.
        kind = self.d.CONST_PLAYLIST_TYPE_INT[self.d.cur_idx]
        a['type'] = kind
        if kind == 'regular':
            f = self.d.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()

            # The parsed YouTube playlist ID.
            playlist_id = StringValidator.get_youtube_playlist_id_from_link(f)
            a['playlist-id'] = playlist_id

        elif kind == 'rss':
            f = self.d.findChild(QtWidgets.QLineEdit, 'field_key').text().strip()
            a['rss-title-keyword'] = f

        if self.action == 'new':
            Lg('main.FramePlaylist.on_dialog_forms_accepted', f'Creating a new playlist entry: {title} ...')

            # Add a new item to the list.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(title)
            self.findChild(QtWidgets.QListWidget, self.active_list).addItem(b)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, self.active_list).setCurrentItem(b)

            # Finally, reconsider item order.
            self.reconsider_playlist_order()

        elif self.action == 'edit':
            Lg('main.FramePlaylist.on_dialog_forms_accepted', f'Editing an existing playlist: {title} ...')

            # Edit the item's title.
            self.cur_item.setText(title)

            # Apply the item's modified data.
            self.cur_item.setData(self.DEFAULT_ITEM_ROLE, a)

            # Finally, reconsider item order.
            self.reconsider_playlist_order()

        # Update the current selection and state.
        if self.active_list == 'list_pinned':
            self.on_list_pinned_item_changed()
        elif self.active_list == 'list_standard':
            self.on_list_standard_item_changed()

    @pyqtSlot()
    def on_list_pinned_item_changed(self):
        if self.findChild(QtWidgets.QListWidget, 'list_pinned').currentItem() is None:
            return

        # Flag this item list as the active one.
        self.active_list = 'list_pinned'

        # Setting the current item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_pinned').currentItem()

        # The selected item's data.
        item_data = self.findChild(QtWidgets.QListWidget, 'list_pinned').currentItem().data(self.DEFAULT_ITEM_ROLE)

        # Enforcing exclusive item list group selection.
        self.findChild(QtWidgets.QListWidget, 'list_standard').setCurrentRow(-1)

        # ------ DISABLING AND ENABLING SORT BUTTONS AS NEEDED ------ #

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_pinned').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_pinned').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_pinned').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(False)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

        # Update the snippet display.
        self.update_snippet_data()

    @pyqtSlot()
    def on_list_standard_item_changed(self):
        if self.findChild(QtWidgets.QListWidget, 'list_standard').currentItem() is None:
            return

        # Flag this item list as the active one.
        self.active_list = 'list_standard'

        # Setting the current item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_standard').currentItem()

        # The selected item's data.
        item_data = self.findChild(QtWidgets.QListWidget, 'list_standard').currentItem().data(self.DEFAULT_ITEM_ROLE)

        # Enforcing exclusive item list group selection.
        self.findChild(QtWidgets.QListWidget, 'list_pinned').setCurrentRow(-1)

        # ------ DISABLING AND ENABLING SORT BUTTONS AS NEEDED ------ #

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_standard').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_standard').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_standard').indexFromItem(a).row()

        if y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

        # Update the snippet display.
        self.update_snippet_data()

    def prefill_fields(self):
        # Redundant preamble logging.
        # Lg('main.FrameGallery.prefill_fields', 'Prefilling gallery data ...')

        # ------------------------- PINNED PLAYLIST ------------------------- #

        # Remove the item list current selection.
        self.findChild(QtWidgets.QListWidget, 'list_pinned').setCurrentRow(-1)
        self.findChild(QtWidgets.QListWidget, 'list_standard').setCurrentRow(-1)

        # Remove previous items to avoid duplication.
        self.findChild(QtWidgets.QListWidget, 'list_pinned').clear()
        self.findChild(QtWidgets.QListWidget, 'list_standard').clear()

        # Iterate through every item in this year.
        for a in self.playlist_dict['pinned']:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(a['title'])
            self.findChild(QtWidgets.QListWidget, 'list_pinned').addItem(b)

            # ------------------------- STANDARD PLAYLIST ------------------------- #

            # Remove the item list current selection.
            self.findChild(QtWidgets.QListWidget, 'list_standard').setCurrentRow(-1)

            # Remove previous items to avoid duplication.
            self.findChild(QtWidgets.QListWidget, 'list_standard').clear()

            # Iterate through every item in this year.
            for a in self.playlist_dict['standard']:
                # Adding the list item.
                b = QtWidgets.QListWidgetItem()
                b.setData(self.DEFAULT_ITEM_ROLE, a)
                b.setText(a['title'])
                self.findChild(QtWidgets.QListWidget, 'list_standard').addItem(b)

    def reconsider_playlist_order(self):
        """
        Rearrange the "playlist_dict" based on the QListItem's item order currently displayed.
        This function overwrites any value previously assigned.
        :return: nothing.
        """
        # ---------------------------- PINNED PLAYLISTS ---------------------------- #

        # Creating the JSON array to replace the old one.
        a = []

        # Reconsider the QListWidget items' orders.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_pinned').__len__()):
            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_pinned').item(i)

            # The item data.
            item_data = b.data(self.DEFAULT_ITEM_ROLE)

            # Add this item to the JSON array.
            a.append(item_data)

        # Overwriting year's value.
        self.playlist_dict['pinned'] = copy.deepcopy(a)

        # ---------------------------- STANDARD PLAYLISTS ---------------------------- #

        # Creating the JSON array to replace the old one.
        a = []

        # Reconsider the QListWidget items' orders.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_standard').__len__()):
            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_standard').item(i)

            # The item data.
            item_data = b.data(self.DEFAULT_ITEM_ROLE)

            # Add this item to the JSON array.
            a.append(item_data)

        # Overwriting year's value.
        self.playlist_dict['standard'] = copy.deepcopy(a)

    def update_snippet_data(self):
        if self.findChild(QtWidgets.QListWidget, self.active_list).currentItem() is None:
            return

        title = self.cur_item.data(self.DEFAULT_ITEM_ROLE)['title']
        kind = self.cur_item.data(self.DEFAULT_ITEM_ROLE)['type']
        kind = 'RSS' if kind == 'rss' else ('Playlist Reguler' if kind == 'regular' else kind)
        last_update = StringValidator.get_full_date(self.cur_item.data(self.DEFAULT_ITEM_ROLE)['last-update'])
        count = str(len(self.cur_item.data(self.DEFAULT_ITEM_ROLE)['content']))

        self.findChild(QtWidgets.QLabel, 'label_title').setText(title)
        self.findChild(QtWidgets.QLabel, 'label_type').setText(kind)
        self.findChild(QtWidgets.QLabel, 'label_count').setText(count)
        self.findChild(QtWidgets.QLabel, 'label_last_update').setText(last_update)
