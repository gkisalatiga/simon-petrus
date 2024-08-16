"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
import os

import global_schema
from handler.dialog.dialog_persembahan import DialogPersembahan
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg
from ui import frame_persembahan


class FramePersembahan(QtWidgets.QFrame, frame_persembahan.Ui_Frame):

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    def __init__(self, *args, obj=None, **kwargs):
        super(FramePersembahan, self).__init__(*args, **kwargs)
        self.action = None
        self.cur_item = None
        self.new_qris_loc = None
        self.qris_loc = None
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogPersembahan(self)

        # Populating the forms list with existing forms.
        self.init_prefilled_banks()

        # Attempt to download the current QRIS image from GitHub, then display the QRIS' pixmap.
        self.init_qris()
        self.reload_qris_pixmap()

        # Add slot connector.
        self.d.accepted.connect(self.on_dialog_banks_accepted)
        self.list_banks.currentItemChanged.connect(self.on_current_item_changed)

    def init_prefilled_banks(self):
        """
        Populate the QListWidget with the bank list found in the GKI Salatiga+ JSON data.
        :return: nothing.
        """
        # Iterating through every list of existing forms in the JSON schema.
        for a in global_schema.app_db.db['offertory']:
            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(
                self.DEFAULT_ITEM_ROLE,
                (a['bank-name'], a['bank-abbr'], a['bank-number'], a['account-holder'])
            )
            b.setText(f'{a["bank-abbr"]} {a["bank-number"]}')
            self.findChild(QtWidgets.QListWidget, 'list_banks').addItem(b)

    def init_qris(self):

        # Using multithreading to prevent GUI freezing [9]
        # (Supress downloading so that the image will not get downloaded on frame change.)
        t = ThreadWithResult(target=global_schema.app_assets.get_main_qris, args=(True,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                qris_loc = t.result
                t.join()

                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()

        # Save the main QRIS path and share it to every member of this class.
        self.qris_loc = qris_loc

    def on_current_item_changed(self):
        # Save the state of the currently selected item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_banks').currentItem()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_banks').__len__()

        # The selected item's index.
        a = self.findChild(QtWidgets.QListWidget, 'list_banks').currentItem()
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(a).row()

        if y_pos == 0:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(False)
        elif y_pos == widget_size - 1:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(False)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_move_down').setEnabled(True)
            self.findChild(QtWidgets.QPushButton, 'btn_move_up').setEnabled(True)

        # Update the display data.
        item_data = self.findChild(QtWidgets.QListWidget, 'list_banks').item(y_pos).data(self.DEFAULT_ITEM_ROLE)
        self.findChild(QtWidgets.QLabel, 'label_bank_name').setText(item_data[0])
        self.findChild(QtWidgets.QLabel, 'label_bank_abbr').setText(item_data[1])
        self.findChild(QtWidgets.QLabel, 'label_number').setText(item_data[2])
        self.findChild(QtWidgets.QLabel, 'label_holder').setText(item_data[3])

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
            self, 'Penghapusan data transfer bank.',
            f'Apakah Anda yakin akan menghapus transfer bank: {title} dari GKI Salatiga+?'
            f'\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(self.cur_item).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_banks').takeItem(y_pos)

            # Logging.
            Lg('main.FramePersembahan.on_btn_delete_clicked', f'Removed the bank info: {title} successfully!')
        else:
            Lg('main.FramePersembahan.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's data.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
        bank_name = item_data[0]
        bank_abbr = item_data[1]
        number = item_data[2].replace('.', '')
        holder = item_data[3]

        # Prompt for user input value.
        self.call_action('edit', bank_abbr, bank_name, number, holder)

    @pyqtSlot()
    def on_btn_export_clicked(self):
        # Ask the user wherein this image should be stored.
        # (Qt5 has built-in overwrite confirmation dialog.)
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        exported_qris = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save the current QRIS image to ...', '', ff)[0]

        if exported_qris == '':
            # Report user cancelled operation.
            QtWidgets.QMessageBox.information(
                self, 'Operation Cancelled!', 'The QRIS image does not get exported.',
                QtWidgets.QMessageBox.Ok
            )

        else:
            Lg('main.FramePersembahan.on_btn_export_clicked', 'Exporting the current QRIS image ...')

            # Read the current QRIS image file as bytes.
            qris_image_as_byte = None
            with open(self.qris_loc, 'rb') as fi:
                qris_image_as_byte = fi.read()

            # Save the file.
            with open(exported_qris, 'wb') as fo:
                fo.write(qris_image_as_byte)

            # Report successful writing.
            QtWidgets.QMessageBox.information(
                self, 'Success!', f'QRIS image has been exported to: {exported_qris}',
                QtWidgets.QMessageBox.Ok
            )

    @pyqtSlot()
    def on_btn_img_select_clicked(self):
        ff = 'Image files (*.bmp *.jpeg *.jpg *.png *.webp)'
        loc = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Pilih media dalam bentuk gambar untuk menggantikan QRIS saat ini', '', ff)[0]

        # Display the currently selected image file for uploading.
        if not loc == '':
            self.new_qris_loc = loc
            img_basename = os.path.basename(loc)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setText(img_basename)
            self.findChild(QtWidgets.QLabel, 'txt_img_loc').setToolTip(loc)

            # Change the QRIS pixmap.
            pixmap = QPixmap(loc)
            self.findChild(QtWidgets.QLabel, 'label_pixmap').setPixmap(pixmap)

    @pyqtSlot()
    def on_btn_move_down_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # The item widget's size.
        widget_size = self.findChild(QtWidgets.QListWidget, 'list_banks').__len__()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == widget_size - 1:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_banks').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos + 1
        self.findChild(QtWidgets.QListWidget, 'list_banks').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_banks').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_move_up_clicked(self):
        if self.cur_item is None:
            return

        # Clone the selected item.
        a = self.cur_item.clone()

        # Get the selected item's row position.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_banks').indexFromItem(self.cur_item).row()

        # Do not move up if already at the top.
        if y_pos == 0:
            return

        # Remove the selected item from the list.
        self.findChild(QtWidgets.QListWidget, 'list_banks').takeItem(y_pos)

        # Move up the item.
        target_pos = y_pos - 1
        self.findChild(QtWidgets.QListWidget, 'list_banks').insertItem(target_pos, a)
        self.findChild(QtWidgets.QListWidget, 'list_banks').setCurrentRow(target_pos)

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Creating the JSON array to replace the old one.
        a = []

        # Iterating through every item.
        for i in range(self.findChild(QtWidgets.QListWidget, 'list_banks').__len__()):

            # The list item.
            b = self.findChild(QtWidgets.QListWidget, 'list_banks').item(i)

            # The item title and URL.
            item_data = b.data(self.DEFAULT_ITEM_ROLE)
            bank_name = item_data[0]
            bank_abbr = item_data[1]
            number = item_data[2]
            holder = item_data[3]

            # Add this item to the JSON array.
            a.append({
                'bank-name': bank_name,
                'bank-abbr': bank_abbr,
                'bank-number': number,
                'account-holder': holder
            })

        # Overwrite the existing forms object.
        global_schema.app_db.db['offertory'] = a

        # Save to local file.
        global_schema.app_db.save_local('offertory')

        # Queue to overwrite the existing QRIS code image file.
        # Only call this expression if there is a newer file selected.
        if self.new_qris_loc is not None:
            global_schema.app_assets.queue_main_qris_change(self.new_qris_loc)

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    def on_dialog_banks_accepted(self):
        # The input dialog's field data.
        bank_name = self.d.findChild(QtWidgets.QLineEdit, 'field_bank_name').text().strip()
        bank_abbr = self.d.findChild(QtWidgets.QLineEdit, 'field_bank_abbr').text().strip()
        number = self.d.findChild(QtWidgets.QLineEdit, 'field_number').text().strip()
        holder = self.d.findChild(QtWidgets.QLineEdit, 'field_holder').text().strip()

        # Visually and string-wise edit the field data to match standard. [11]
        bank_abbr = bank_abbr.upper()

        s = [w for w in number]
        s.insert(3, '.') if len(s) >= 3 else s
        s.insert(6, '.') if len(s) >= 6 else s
        s.insert(10, '.') if len(s) >= 10 else s
        number = ''.join(s)

        # The display title.
        display_text = f'{bank_abbr} {number}'

        if self.action == 'new':
            Lg('main.FramePersembahan.on_dialog_banks_accepted', f'Creating a new bank: {display_text} ...')

            # Add a new item to the list.
            # Adding the list item.
            a = QtWidgets.QListWidgetItem()
            a.setData(
                self.DEFAULT_ITEM_ROLE,
                (bank_name, bank_abbr, number, holder)
            )
            a.setText(display_text)
            self.findChild(QtWidgets.QListWidget, 'list_banks').addItem(a)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_banks').setCurrentItem(a)

        elif self.action == 'edit':
            Lg('main.FramePersembahan.on_dialog_forms_accepted', f'Editing an existing bank info: {display_text} ...')

            # Edit the selected item's value.
            self.cur_item.setText(display_text)
            self.cur_item.setData(
                self.DEFAULT_ITEM_ROLE,
                (bank_name, bank_abbr, number, holder)
            )

        # Update the current selection and state.
        self.on_current_item_changed()

    def reload_qris_pixmap(self):
        """ Reload the QRIS Pixmap in this frame's main display. [12] """
        if os.path.isfile(self.qris_loc) and global_schema.cur_fragment == 'fragment_persembahan':
            Lg('main.FramePersembahan.reload_qris_pixmap', f'Displaying the QRIS image from path: {self.qris_loc} ...')
            pixmap = QPixmap(self.qris_loc)
            self.label_pixmap.setPixmap(pixmap)

    def call_action(self, action,
                    edit_bank_abbr: str = '',
                    edit_bank_name: str = '',
                    edit_number: str = '',
                    edit_holder: str = ''):
        """
        Determine what bank action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the bank action to undergo.
        :param edit_bank_abbr: (optional) the current bank's abbreviation to edit.
        :param edit_bank_name: (optional) the current bank's full name to edit.
        :param edit_number: (optional) the current bank's account number to edit.
        :param edit_holder: (optional) the current bank's account holder to edit.
        :return: nothing.
        """
        self.action = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Info Transfer Bank Baru')

            # Clear the existing title and URL.
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_abbr').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_name').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_number').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_holder').setText('')

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Info Transfer Bank')

            # Prefill with existing values.
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_abbr').setText(edit_bank_abbr)
            self.d.findChild(QtWidgets.QLineEdit, 'field_bank_name').setText(edit_bank_name)
            self.d.findChild(QtWidgets.QLineEdit, 'field_number').setText(edit_number)
            self.d.findChild(QtWidgets.QLineEdit, 'field_holder').setText(edit_holder)

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_fields()
