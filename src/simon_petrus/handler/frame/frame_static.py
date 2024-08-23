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
from handler.dialog.dialog_static_content import DialogStaticContent
from handler.dialog.dialog_static_folder import DialogStaticFolder
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from lib.string_validator import StringValidator
from ui import frame_static


class FrameStatic(QtWidgets.QFrame, frame_static.Ui_Frame):

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    def __init__(self, *args, obj=None, **kwargs):
        super(FrameStatic, self).__init__(*args, **kwargs)
        self.action_content = None
        self.action_folder = None
        self.cur_item_folder = None
        self.cur_item_content = None
        self.setupUi(self)

        # Initiating the prompt dialogs.
        self.f = DialogStaticFolder(self)
        self.c = DialogStaticContent(self)

        # Copy all things in the original dict.
        self.static_dict = copy.deepcopy(global_schema.app_assets.static)

        # DEBUG.
        # print('0x123', self.static_dict)

        # Prefill with information.
        self.prefill_fields()

        # Connect the slots.
        self.c.accepted.connect(self.on_dialog_content_accepted)
        self.f.accepted.connect(self.on_dialog_folder_accepted)
        self.list_static_content.currentItemChanged.connect(self.on_list_static_content_changed)
        self.list_static_folder.currentItemChanged.connect(self.on_list_static_folder_changed)

    def call_action_content(self, action, edit_title: str = '', edit_subtitle: str = '', edit_url: str = '', edit_html: str = ''):
        """
        Determine what static content action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the gallery action to undergo.
        :param edit_title: (optional) the current static content's title to edit.
        :param edit_subtitle: (optional) the current static content's subtitle to edit.
        :param edit_url: (optional) the current static content's image url to edit.
        :param edit_html: (optional) the current static content's HTML content to edit.
        :return: nothing.
        """
        self.action_content = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.c.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Konten Baru')

            # Clear the existing title and URL.
            self.c.findChild(QtWidgets.QLineEdit, 'field_title').setText('')
            self.c.findChild(QtWidgets.QLineEdit, 'field_subtitle').setText('')
            self.c.findChild(QtWidgets.QLineEdit, 'field_url').setText('')
            self.c.findChild(QtWidgets.QPlainTextEdit, 'editor_main').setPlainText('')

        elif action == 'edit':
            self.c.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Konten')

            # Prefill with existing values.
            self.c.findChild(QtWidgets.QLineEdit, 'field_title').setText(edit_title)
            self.c.findChild(QtWidgets.QLineEdit, 'field_subtitle').setText(edit_subtitle)
            self.c.findChild(QtWidgets.QLineEdit, 'field_url').setText(edit_url)
            self.c.findChild(QtWidgets.QPlainTextEdit, 'editor_main').setPlainText(edit_html)

        # Show the dialog.
        self.c.show()

        # Validate preliminary field values.
        self.c.validate_fields()

    def call_action_folder(self, action, edit_title: str = '', edit_url: str = ''):
        """
        Determine what static folder action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the gallery action to undergo.
        :param edit_title: (optional) the current static folder's title to edit.
        :param edit_url: (optional) the current static folder's banner url to edit.
        :return: nothing.
        """
        self.action_folder = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.f.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Folder Konten Baru')

            # Clear the existing title and URL.
            self.f.findChild(QtWidgets.QLineEdit, 'field_title').setText('')
            self.f.findChild(QtWidgets.QLineEdit, 'field_url').setText('')

        elif action == 'edit':
            self.f.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Folder Konten')

            # Prefill with existing values.
            self.f.findChild(QtWidgets.QLineEdit, 'field_title').setText(edit_title)
            self.f.findChild(QtWidgets.QLineEdit, 'field_url').setText(edit_url)

        # Show the dialog.
        self.f.show()

        # Validate preliminary field values.
        self.f.validate_fields()

    @pyqtSlot()
    def on_btn_add_content_clicked(self):
        # Prompt for user input value.
        self.call_action_content('new')

    @pyqtSlot()
    def on_btn_add_folder_clicked(self):
        # Prompt for user input value.
        self.call_action_folder('new')

    @pyqtSlot()
    def on_btn_delete_content_clicked(self):
        if self.cur_item_content is None:
            return

        # The title of the currently selected item.
        title = self.cur_item_content.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan konten.',
            f'Apakah Anda yakin akan menghapus konten: {title}?\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_content').indexFromItem(self.cur_item_content).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_static_content').takeItem(y_pos)

            # Finally, consider content order.
            self.reconsider_static_order()

            # Logging.
            Lg('main.FrameStatic.on_btn_delete_content_clicked', f'Removed the content: {title} successfully!')
        else:
            Lg('main.FrameStatic.on_btn_delete_content_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_delete_folder_clicked(self):
        if self.cur_item_folder is None:
            return

        # The title of the currently selected item.
        title = self.cur_item_folder.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data folder konten.',
            f'Apakah Anda yakin akan menghapus folder konten: {title}?\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_folder').indexFromItem(self.cur_item_folder).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_static_folder').takeItem(y_pos)

            # Logging.
            Lg('main.FrameStatic.on_btn_delete_folder_clicked', f'Removed the folder: {title} successfully!')
        else:
            Lg('main.FrameStatic.on_btn_delete_folder_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_content_clicked(self):
        if self.cur_item_content is None:
            return

        # The selected item's inherent data.
        item_data = self.cur_item_content.data(self.DEFAULT_ITEM_ROLE)

        # The selected item's title and url.
        title = item_data['title']
        subtitle = item_data['subtitle']
        url = item_data['featured-image']
        html = item_data['html']

        # Prompt for user input value.
        self.call_action_content('edit', title, subtitle, url, html)

    @pyqtSlot()
    def on_btn_edit_folder_clicked(self):
        if self.cur_item_folder is None:
            return

        # The selected item's inherent data.
        item_data = self.cur_item_folder.data(self.DEFAULT_ITEM_ROLE)

        # The selected item's title and url.
        title = item_data['title']
        url = item_data['banner']

        # Prompt for user input value.
        self.call_action_folder('edit', title, url)

    @pyqtSlot()
    def on_btn_move_down_content_clicked(self):
        if self.cur_item_content is None:
            return

        # Clone the selected item.
        a = self.cur_item_content.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_static_content').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_content').indexFromItem(self.cur_item_content).row()

        # Do not move up if already at the bottom.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_static_content').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_static_content').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_static_content').setCurrentRow(target_pos)

        # Finally, consider content order.
        self.reconsider_static_order()

    @pyqtSlot()
    def on_btn_move_down_folder_clicked(self):
        if self.cur_item_folder is None:
            return

        # Clone the selected item.
        a = self.cur_item_folder.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_static_folder').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_folder').indexFromItem(self.cur_item_folder).row()

        # Do not move up if already at the bottom.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_static_folder').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_static_folder').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_static_folder').setCurrentRow(target_pos)

        # No need to reconsider folder order.
        # It will only be done when the user clicks "save".

    @pyqtSlot()
    def on_btn_move_up_content_clicked(self):
        if self.cur_item_content is None:
            return

        # Clone the selected item.
        a = self.cur_item_content.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_content').indexFromItem(self.cur_item_content).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_static_content').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_static_content').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_static_content').setCurrentRow(target_pos)

        # Finally, consider content order.
        self.reconsider_static_order()

    @pyqtSlot()
    def on_btn_move_up_folder_clicked(self):
        if self.cur_item_folder is None:
            return

        # Clone the selected item.
        a = self.cur_item_folder.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_folder').indexFromItem(self.cur_item_folder).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_static_folder').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_static_folder').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_static_folder').setCurrentRow(target_pos)

        # No need to reconsider folder order.
        # It will only be done when the user clicks "save".

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Creating the JSON array to replace the old one.
        a = []

        # Iterating through every item.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_static_folder').__len__()):
            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_static_folder').item(i)

            # The item data.
            item_data = b.data(self.DEFAULT_ITEM_ROLE)

            # Add this item to the JSON array.
            a.append(item_data)

        # Overwrite the existing static content object.
        global_schema.app_assets.static = copy.deepcopy(a)

        # Save to local file.
        global_schema.app_assets.save_local_static()

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    @pyqtSlot()
    def on_dialog_content_accepted(self):
        # The input dialog's title, URL, and story fields.
        title = self.c.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        subtitle = self.c.findChild(QtWidgets.QLineEdit, 'field_subtitle').text().strip()
        url = self.c.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()
        html = self.c.findChild(QtWidgets.QPlainTextEdit, 'editor_main').toPlainText().strip()

        if self.action_content == 'new':
            Lg('main.FrameStatic.on_dialog_content_accepted', f'Creating a new content: {title} ...')

            # Creating a new JSON data.
            a = {
                'title': title,
                'subtitle': subtitle,
                'featured-image': url,
                'html': html
            }

            # Add a new item to the list.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(title)
            self.findChild(QtWidgets.QListWidget, 'list_static_content').addItem(b)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_static_content').setCurrentItem(b)

            # Finally, reconsider content order.
            self.reconsider_static_order()

        elif self.action_content == 'edit':
            Lg('main.FrameStatic.on_dialog_content_accepted', f'Editing an existing content: {title} ...')

            # Edit the selected item's value.
            item_data = self.cur_item_content.data(self.DEFAULT_ITEM_ROLE)
            item_data['title'] = title
            item_data['subtitle'] = subtitle
            item_data['featured-image'] = url
            item_data['html'] = html

            # Edit the item's title.
            self.cur_item_content.setText(title)

            # Apply the item's modified data.
            self.cur_item_content.setData(self.DEFAULT_ITEM_ROLE, item_data)

            # Finally, reconsider content order.
            self.reconsider_static_order()

        # Update the current selection and state.
        self.on_list_static_content_changed()

    @pyqtSlot()
    def on_dialog_folder_accepted(self):
        # The input dialog's title, URL, and story fields.
        title = self.f.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.f.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()

        if self.action_folder == 'new':
            Lg('main.FrameStatic.on_dialog_folder_accepted', f'Creating a new folder: {title} ...')

            # Creating a new JSON data.
            a = {
                'title': title,
                'banner': url,
                'content': []
            }

            # Add a new item to the list.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(title)
            self.findChild(QtWidgets.QListWidget, 'list_static_folder').addItem(b)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_static_folder').setCurrentItem(b)

            # No need to reconsider folder order.
            # It will only be done when the user clicks "save".

        elif self.action_folder == 'edit':
            Lg('main.FrameStatic.on_dialog_folder_accepted', f'Editing an existing folder: {title} ...')

            # Edit the selected item's value.
            item_data = self.cur_item_folder.data(self.DEFAULT_ITEM_ROLE)
            item_data['title'] = title
            item_data['banner'] = url

            # Edit the item's title.
            self.cur_item_folder.setText(title)

            # Apply the item's modified data.
            self.cur_item_folder.setData(self.DEFAULT_ITEM_ROLE, item_data)

            # No need to reconsider folder order.
            # It will only be done when the user clicks "save".

        # Update the current selection and state.
        self.on_list_static_folder_changed()

    @pyqtSlot()
    def on_list_static_content_changed(self):
        # The selected folder.
        self.cur_item_content = self.findChild(QtWidgets.QListWidget, 'list_static_content').currentItem()

        if self.cur_item_content == '' or self.cur_item_content is None:
            return

        # ------ DISABLING AND ENABLING SORT BUTTONS AS NEEDED ------ #

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_static_content').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_static_content').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_content').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down_content').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up_content').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down_content').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up_content').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down_content').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up_content').setEnabled(True)

    @pyqtSlot()
    def on_list_static_folder_changed(self):
        # The selected folder.
        self.cur_item_folder = self.findChild(QtWidgets.QListWidget, 'list_static_folder').currentItem()

        if self.cur_item_folder == '' or self.cur_item_folder is None:
            return

        # The selected folder's loaded content.
        folder_load = self.cur_item_folder.data(self.DEFAULT_ITEM_ROLE)

        # Display basic information about the folder.
        self.findChild(QtWidgets.QLabel, 'label_folder_title').setText(folder_load['title'])
        self.findChild(QtWidgets.QLabel, 'label_folder_url').setText(folder_load['banner'])
        self.findChild(QtWidgets.QLabel, 'label_folder_url').setToolTip(folder_load['banner'])

        # Remove the item list current selection.
        self.findChild(QtWidgets.QListWidget, 'list_static_content').setCurrentRow(-1)

        # Remove previous items to avoid duplication.
        self.findChild(QtWidgets.QListWidget, 'list_static_content').clear()

        # Iterate through every item in the selected item in "static folder".
        for a in folder_load['content']:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(a['title'])
            self.findChild(QtWidgets.QListWidget, 'list_static_content').addItem(b)

        # ------ DISABLING AND ENABLING SORT BUTTONS AS NEEDED ------ #

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_static_folder').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_static_folder').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_static_folder').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down_folder').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up_folder').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down_folder').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up_folder').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down_folder').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up_folder').setEnabled(True)

    def prefill_fields(self):
        # Redundant preamble logging.
        # Lg('main.FrameStatic.prefill_fields', 'Prefilling gallery data ...')

        # Remove any previous items in the folder list.
        self.findChild(QtWidgets.QListWidget, 'list_static_folder').clear()

        # Fill in the year combo box field.
        for a in self.static_dict:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(self.DEFAULT_ITEM_ROLE, a)
            b.setText(a['title'])
            self.findChild(QtWidgets.QListWidget, 'list_static_folder').addItem(b)

        # Update the main list item display.
        self.on_list_static_folder_changed()

    def reconsider_static_order(self):
        """
        Rearrange the "static_dict" based on the QListItem's item order currently displayed.
        This function overwrites any value previously assigned to "self.static_dict[key]".
        :return: nothing.
        """
        # The selected static folder.
        folder = self.findChild(QtWidgets.QListWidget, 'list_static_folder').currentItem()

        # The selected static folder's data.
        folder_data = folder.data(self.DEFAULT_ITEM_ROLE)

        # Creating the JSON array to replace the old one.
        a = []

        # Reconsider the QListWidget items' orders.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_static_content').__len__()):
            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_static_content').item(i)

            # The item data.
            item_data = b.data(self.DEFAULT_ITEM_ROLE)

            # Add this item to the JSON array.
            a.append(item_data)

        # Overwriting content's value.
        folder_data['content'] = copy.deepcopy(a)
        folder.setData(self.DEFAULT_ITEM_ROLE, folder_data)
