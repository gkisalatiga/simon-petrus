"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

import global_schema
from handler.dialog.dialog_forms import DialogForms
from lib.logger import Logger as Lg
from ui import frame_formulir


class FrameFormulir(QtWidgets.QFrame, frame_formulir.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameFormulir, self).__init__(*args, **kwargs)
        self.action = ''
        self.cur_item = QtWidgets.QListWidgetItem()
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogForms(self)

        # Populating the forms list with existing forms.
        self.init_prefilled_forms()

        # Add slot connector.
        self.d.accepted.connect(self.on_dialog_forms_accepted)
        self.list_forms.currentItemChanged.connect(self.on_current_item_changed)

    def init_prefilled_forms(self):
        """
        Populate the QListWidget with the forms list found in the GKI Salatiga+ JSON data.
        :return: nothing.
        """
        # Iterating through every list of existing forms in the JSON schema.
        for a in global_schema.app_db.db['forms']:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setText(a['title'])
            b.setToolTip(a['url'])
            self.findChild(QtWidgets.QListWidget, 'list_forms').addItem(b)

    @pyqtSlot()
    def on_btn_add_clicked(self):
        # Prompt for user input value.
        self.call_action('new')

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        if self.cur_item is None:
            return

        # The title of the currently selected item.
        title = self.cur_item.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data formulir.',
            f'Apakah Anda yakin akan menghapus formulir: {title}?\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(self.cur_item).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_forms').takeItem(y_pos)

            # Logging.
            Lg('main.FrameFormulir.on_btn_delete_clicked', f'Removed the form: {title} successfully!')
        else:
            Lg('main.FrameFormulir.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's title and url.
        title = self.cur_item.text()
        url = self.cur_item.toolTip()

        # Prompt for user input value.
        self.call_action('edit', title, url)

    @pyqtSlot()
    def on_btn_move_down_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_forms').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_forms').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_forms').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_forms').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_move_up_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_forms').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_forms').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_forms').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Creating the JSON array to replace the old one.
        a = []

        # Iterating through every item.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_forms').__len__()):

            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_forms').item(i)

            # The item title and URL.
            title = b.text()
            url = b.toolTip()

            # Add this item to the JSON array.
            a.append({
                'title': title,
                'url': url
            })

        # Overwrite the existing forms object.
        global_schema.app_db.db['forms'] = a

        # Save to local file.
        global_schema.app_db.save_local('forms')

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    def on_current_item_changed(self):
        # Save the state of the currently selected item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_forms').currentItem()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_forms').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_forms').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_forms').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

    @pyqtSlot()
    def on_dialog_forms_accepted(self):
        # The input dialog's title and URL fields.
        title = self.d.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        url = self.d.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()

        if self.action == 'new':
            Lg('main.FrameFormulir.on_dialog_forms_accepted', f'Creating a new form: {title} ...')

            # Add a new item to the list.
            a = QtWidgets.QListWidgetItem()
            a.setText(title)
            a.setToolTip(url)
            self.findChild(QtWidgets.QListWidget, 'list_forms').addItem(a)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_forms').setCurrentItem(a)

        elif self.action == 'edit':
            Lg('main.FrameFormulir.on_dialog_forms_accepted', f'Editing an existing form: {title} ...')

            # Edit the selected item's value.
            self.cur_item.setText(title)
            self.cur_item.setToolTip(url)

        # Update the current selection and state.
        self.on_current_item_changed()

    def call_action(self, action, edit_title: str = '', edit_url: str = ''):
        """
        Determine what forms action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the forms action to undergo.
        :param edit_title: (optional) the current form's title to edit.
        :param edit_url: (optional) the current form's url to edit.
        :return: nothing.
        """
        self.action = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Formulir Baru')

            # Clear the existing title and URL.
            self.d.findChild(QtWidgets.QLineEdit, 'field_title').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_url').setText('')

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Formulir')

            # Prefill with existing values.
            self.d.findChild(QtWidgets.QLineEdit, 'field_title').setText(edit_title)
            self.d.findChild(QtWidgets.QLineEdit, 'field_url').setText(edit_url)

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_fields()
