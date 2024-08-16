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
from handler.dialog.dialog_gallery import DialogGallery
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from lib.string_validator import StringValidator
from ui import frame_gallery


class FrameGallery(QtWidgets.QFrame, frame_gallery.Ui_Frame):

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    def __init__(self, *args, obj=None, **kwargs):
        super(FrameGallery, self).__init__(*args, **kwargs)
        self.action = None
        self.cur_item = None
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogGallery(self)

        # Copy all things in the original dict.
        self.gallery_dict = copy.deepcopy(global_schema.app_assets.gallery)

        # Prefill with information.
        self.prefill_fields()

        # Connect the slots.
        self.d.accepted.connect(self.on_dialog_forms_accepted)
        self.combo_year.currentIndexChanged.connect(self.on_combo_year_index_changed)
        self.list_gallery.currentItemChanged.connect(self.on_list_gallery_item_changed)

    def call_action(self, action, edit_title: str = '', edit_url: str = '', edit_story: str = ''):
        """
        Determine what gallery action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the gallery action to undergo.
        :param edit_title: (optional) the current gallery folder's title to edit.
        :param edit_url: (optional) the current gallery folder's url to edit.
        :param edit_story: (optional) the current gallery folder's story to edit.
        :return: nothing.
        """
        self.action = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Folder Album Baru')

            # Clear the existing title and URL.
            self.d.findChild(QtWidgets.QLineEdit, 'field_title').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_url').setText('')
            self.d.findChild(QtWidgets.QPlainTextEdit, 'field_story').setPlainText('')

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Folder Album')

            # Prefill with existing values.
            self.d.findChild(QtWidgets.QLineEdit, 'field_title').setText(edit_title)
            self.d.findChild(QtWidgets.QLineEdit, 'field_url').setText(edit_url)
            self.d.findChild(QtWidgets.QPlainTextEdit, 'field_story').setPlainText(edit_story)

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_fields()

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
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_gallery').indexFromItem(self.cur_item).row()

            # Get the selected year album.
            year = self.findChild(QtWidgets.QComboBox, 'combo_year').currentText()

            # The selected item's data in the gallery dict.
            item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)

            # Remove from the class' gallery dict.
            self.gallery_dict[year].remove(item_data)

            # Remove also the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_gallery').takeItem(y_pos)

            # Logging.
            Lg('main.FrameGallery.on_btn_delete_clicked', f'Removed the form: {title} successfully!')
        else:
            Lg('main.FrameGallery.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's inherent data.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)

        # The selected item's title and url.
        title = item_data['title']
        url = 'https://drive.google.com/drive/folders/' + item_data['folder_id']
        story = item_data['story']

        # Prompt for user input value.
        self.call_action('edit', title, url, story)

    @pyqtSlot()
    def on_btn_fetch_clicked(self):
        # The currently selected item's Google Drive folder ID.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
        title = item_data['title']
        folder_id = item_data['folder_id']

        # Disable all elements in this window, to prevent user input.
        global_schema.disable_widget(global_schema.win_main)

        # Using multithreading to prevent GUI freezing [9]
        # (Supress downloading so that the image will not get downloaded on frame change.)
        t = ThreadWithResult(target=global_schema.app_assets.get_gdrive_folder_list, args=(folder_id,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                all_files = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Set last update value.
        item_data['last_update'] = StringValidator.get_date()

        # Apply the retrieved data to the currently selected item.
        a = []
        for b in all_files:
            if b['mimeType'].startswith('image/'):
                a.append({
                    'id': b['id'],
                    'name': b['name'],
                    'date': b['createdTime'].split('T')[0]
                })

        # Overwriting the item's data.
        item_data['photos'] = copy.deepcopy(a)
        self.cur_item.setData(self.DEFAULT_ITEM_ROLE, item_data)

        # Re-enable all elements in this window.
        global_schema.enable_widget(global_schema.win_main)

        # Recalculate items and displays.
        self.on_list_gallery_item_changed()
        self.reconsider_album_order()

        # Notify the user about successful fetching.
        QtWidgets.QMessageBox.information(
            self, 'Berhasil memutakhirkan data album!', f'Berhasil memutakhirkan data isi konten dari album: {title}',
            QtWidgets.QMessageBox.Ok
        )

    @pyqtSlot()
    def on_btn_move_down_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_gallery').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_gallery').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_gallery').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_gallery').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_gallery').setCurrentRow(target_pos)

        # Finally, reconsider album order.
        self.reconsider_album_order()

    @pyqtSlot()
    def on_btn_move_up_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_gallery').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_gallery').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_gallery').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_gallery').setCurrentRow(target_pos)

        # Finally, reconsider album order.
        self.reconsider_album_order()

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Overwrite the existing forms object.
        global_schema.app_assets.gallery = copy.deepcopy(self.gallery_dict)

        # Save to local file.
        global_schema.app_assets.save_local_gallery()

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    @pyqtSlot()
    def on_btn_year_del_clicked(self):
        len_keys = len(self.gallery_dict.keys())
        if len_keys - 1 <= 0:
            # Warn the user about what is being done.
            delete = QtWidgets.QMessageBox.warning(
                self, 'Tidak dapat menghapus album', f'Minimum harus ada satu album yang aktif!',
                QtWidgets.QMessageBox.Ok
            )
            return

        year = self.findChild(QtWidgets.QComboBox, 'combo_year').currentText()
        # Warn the user about what is being done.
        delete = QtWidgets.QMessageBox.warning(
            self, 'Yakin menghapus?', f'Apakah Anda yakin ingin menghapus album "Tahun {year}"?'
                                      f'Aksi ini tidak akan dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if delete == QtWidgets.QMessageBox.Yes:
            self.gallery_dict.__delitem__(year)
            Lg('main.FrameGallery.on_btn_year_del_clicked', f'Removed: {year}')
            # Report user finished operation.
            QtWidgets.QMessageBox.information(
                self, 'Berhasil menghapus!', f'Album "Tahun {year}" berhasil dihapus!',
                QtWidgets.QMessageBox.Ok
            )
        else:
            Lg('main.FrameGallery.on_btn_year_del_clicked', f'Phew! The year {year} carries on!')

        # Recalculate the display.
        self.prefill_fields()
        self.on_combo_year_index_changed()
        self.on_list_gallery_item_changed()

    @pyqtSlot()
    def on_btn_year_new_clicked(self):
        # Add the year to the database schema.
        year = self.findChild(QtWidgets.QDateEdit, 'new_year').text()
        if not self.gallery_dict.keys().__contains__(year):
            self.gallery_dict[year] = []
            # Report user finished operation.
            QtWidgets.QMessageBox.information(
                self, 'Berhasil membuat album!', f'Album "Tahun {year}" berhasil dibuat!',
                QtWidgets.QMessageBox.Ok
            )
        else:
            # Report user failed operation.
            QtWidgets.QMessageBox.warning(
                self, 'Galat!', f'Album "Tahun {year}" sudah pernah dibuat sebelumnya. Coba nama lain!',
                QtWidgets.QMessageBox.Ok
            )

        # Now add the combo box item, among other things.
        self.prefill_fields()

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
        for a in self.gallery_dict[year]:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(a['title'])
            self.findChild(QtWidgets.QListWidget, 'list_gallery').addItem(b)

    @pyqtSlot()
    def on_dialog_forms_accepted(self):
        # The input dialog's title, URL, and story fields.
        title = self.d.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.d.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()
        story = self.d.findChild(QtWidgets.QPlainTextEdit, 'field_story').toPlainText().strip()

        # The parsed Google Drive folder ID.
        folder_id = urlparse(url).path.split('/')[-1]

        if self.action == 'new':
            Lg('main.FrameGallery.on_dialog_forms_accepted', f'Creating a new album: {title} ...')

            # Creating a new JSON data.
            a = {
                'title': title,
                'folder_id': folder_id,
                'last_update': '',
                'story': story,
                'photos': []
            }

            # Add a new item to the list.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(title)
            self.findChild(QtWidgets.QListWidget, 'list_gallery').addItem(b)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_gallery').setCurrentItem(b)

            # Finally, reconsider item order.
            self.reconsider_album_order()

        elif self.action == 'edit':
            Lg('main.FrameGallery.on_dialog_forms_accepted', f'Editing an existing album: {title} ...')

            # Edit the selected item's value.
            item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            item_data['title'] = title
            item_data['folder_id'] = folder_id
            item_data['story'] = story

            # Edit the item's title.
            self.cur_item.setText(title)

            # Apply the item's modified data.
            self.cur_item.setData(self.DEFAULT_ITEM_ROLE, item_data)

            # Finally, reconsider item order.
            self.reconsider_album_order()

        # Update the current selection and state.
        self.on_list_gallery_item_changed()

    @pyqtSlot()
    def on_list_gallery_item_changed(self):
        if self.findChild(QtWidgets.QListWidget, 'list_gallery').currentItem() is None:
            return

        # Setting the current item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_gallery').currentItem()

        # The selected item's data.
        item_data = self.findChild(QtWidgets.QListWidget, 'list_gallery').currentItem().data(self.DEFAULT_ITEM_ROLE)

        # The number of contents in this item.
        count = len(item_data['photos'])

        # The Google Drive link of this item's folder.
        url = StringValidator.get_gdrive_full_url(item_data['folder_id'])

        # The last time this album gets updated.
        last_update = 'Tidak Pernah' if item_data['last_update'] == '' else StringValidator.get_full_date(
            item_data['last_update']
        )

        # Displaying the item's data to the respective label/fields.
        self.findChild(QtWidgets.QLabel, 'label_name').setText(item_data['title'])
        self.findChild(QtWidgets.QLabel, 'label_id').setText(item_data['folder_id'])
        self.findChild(QtWidgets.QLabel, 'label_count').setText(str(count))
        self.findChild(QtWidgets.QLabel, 'label_last_update').setText(last_update)
        self.findChild(QtWidgets.QLabel, 'label_url').setText(url)
        self.findChild(QtWidgets.QLabel, 'label_url').setToolTip(url)
        self.findChild(QtWidgets.QLabel, 'label_story').setText(item_data['story'])

        # ------ DISABLING AND ENABLING SORT BUTTONS AS NEEDED ------ #

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_gallery').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_gallery').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_gallery').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

    def prefill_fields(self):
        # Redundant preamble logging.
        # Lg('main.FrameGallery.prefill_fields', 'Prefilling gallery data ...')

        # Remove any previous items in the combo box.
        self.findChild(QtWidgets.QComboBox, 'combo_year').clear()

        # Fill in the year combo box field.
        for a in sorted(self.gallery_dict.keys()):
            self.findChild(QtWidgets.QComboBox, 'combo_year').addItem(a)

        # Update the main list item display.
        self.on_combo_year_index_changed()

    def reconsider_album_order(self):
        """
        Rearrange the "gallery_dict" based on the QListItem's item order currently displayed.
        This function overwrites any value previously assigned to "self.gallery_dict[year]".
        :return: nothing.
        """
        # The selected year.
        year = self.findChild(QtWidgets.QComboBox, 'combo_year').currentText()

        # Creating the JSON array to replace the old one.
        a = []

        # Reconsider the QListWidget items' orders.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_gallery').__len__()):
            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_gallery').item(i)

            # The item data.
            item_data = b.data(self.DEFAULT_ITEM_ROLE)

            # Add this item to the JSON array.
            a.append(item_data)

        # Overwriting year's value.
        self.gallery_dict[year] = copy.deepcopy(a)
