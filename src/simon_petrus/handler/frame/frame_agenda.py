"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTime
import copy

from handler.dialog.dialog_agenda import DialogAgenda
from lib.logger import Logger as Lg
from lib.string_validator import StringValidator
from ui import frame_agenda
import global_schema


class FrameAgenda(QtWidgets.QFrame, frame_agenda.Ui_Frame):

    # The QListWidgetItem default role.
    DEFAULT_ITEM_ROLE = 1048577  # --- 2**20 + 1

    # The dict key for each day of the week.
    DAY_OF_WEEK_KEY = [
        'mon',
        'tue',
        'wed',
        'thu',
        'fri',
        'sat',
        'sun'
    ]

    def __init__(self, *args, obj=None, **kwargs):
        super(FrameAgenda, self).__init__(*args, **kwargs)
        self.action = None
        self.cur_day_int = 0  # --- the default.
        self.cur_item = None
        self.setupUi(self)

        # Initiating the prompt dialog.
        self.d = DialogAgenda(self)

        # Initiate inital values according to the original, non-edited JSON schema.
        self.agenda_dict = copy.deepcopy(global_schema.app_db.db['agenda'])

        # Initialize the initial values.
        self.prefill_list_items()

        # Initialize the day title.
        self.change_day_title()

        # Add slot connector.
        self.d.accepted.connect(self.on_dialog_agenda_accepted)
        self.day_selector.currentChanged.connect(self.on_day_selector_value_change)
        self.list_agenda.currentItemChanged.connect(self.on_current_item_changed)

    def change_day_title(self):
        the_day = StringValidator.LOCALE_DAY_OF_WEEK[self.cur_day_int]
        self.findChild(QtWidgets.QLabel, 'app_title').setText(f'Jadwal Sepekan: Hari {the_day}')

    @pyqtSlot()
    def on_btn_add_clicked(self):
        # Prompt for user input value.
        the_day = StringValidator.LOCALE_DAY_OF_WEEK[self.cur_day_int]
        self.call_action('new', the_day)

    @pyqtSlot()
    def on_btn_delete_clicked(self):
        if self.cur_item is None:
            return

        # The title of the currently selected item.
        title = self.cur_item.text()

        # Warn the user about deletion.
        r = (QtWidgets.QMessageBox.warning(
            self, 'Penghapusan data agenda.',
            f'Apakah Anda yakin akan menghapus agenda: {title} dari GKI Salatiga+?'
            f'\nTindakan ini tidak dapat dikembalikan!',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ))

        # Validating the response.
        if r == QtWidgets.QMessageBox.Yes:
            # The old data.
            old_item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            old_day = old_item_data[0]
            old_name = old_item_data[1]
            old_time = old_item_data[2]
            old_place = old_item_data[3]
            old_representative = old_item_data[4]
            old_order = old_item_data[5]

            # Find the index of this item.
            idx = self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].index({
                'name': old_name,
                'time': old_time,
                'place': old_place,
                'representative': old_representative
            })

            # Now we find the new index order of this item.
            order = idx

            # Remove this item from the agenda dict.
            self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].__delitem__(order)

            # Get the selected item's row position.
            y_pos = self.findChild(QtWidgets.QListWidget, 'list_agenda').indexFromItem(self.cur_item).row()

            # Remove the selected item from the list.
            self.findChild(QtWidgets.QListWidget, 'list_agenda').takeItem(y_pos)

            # Logging.
            Lg('main.FrameAgenda.on_btn_delete_clicked', f'Removed the agenda info: {title} successfully!')
        else:
            Lg('main.FrameAgenda.on_btn_delete_clicked', f'Phew! It did not get removed.')

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        if self.cur_item is None:
            return

        # The selected item's data.
        item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
        day = StringValidator.LOCALE_DAY_OF_WEEK[self.DAY_OF_WEEK_KEY.index(item_data[0])]
        name = item_data[1]
        time = item_data[2]
        place = item_data[3]
        representative = item_data[4]
        order = item_data[5]

        # Prompt for user input value.
        self.call_action('edit', day, name, time, place, representative, order)

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # Overwrite the existing forms object.
        global_schema.app_db.db['agenda'] = self.agenda_dict

        # Save to local file.
        global_schema.app_db.save_local('agenda')

        # Display the save successful notice.
        QtWidgets.QMessageBox.information(
            self, 'Data tersimpan!',
            'Perubahan data berhasil disimpan. Silahkan unggah pembaruan supaya data dapat dilihat oleh jemaat.',
            QtWidgets.QMessageBox.Ok
        )

    def on_current_item_changed(self):
        # Save the state of the currently selected item.
        self.cur_item = self.findChild(QtWidgets.QListWidget, 'list_agenda').currentItem()

        # The QListWidgetItem object of the selected item.
        a = self.findChild(QtWidgets.QListWidget, 'list_agenda').currentItem()
        if a == None:
            return

        # The selected item's index.
        y_pos = self.findChild(QtWidgets.QListWidget, 'list_agenda').indexFromItem(a).row()

        # Change the non-user-editable field display.
        the_day = StringValidator.LOCALE_DAY_OF_WEEK[self.cur_day_int]
        self.findChild(QtWidgets.QLabel, 'label_day').setText(the_day)

        # Update the display data.
        item_data = self.findChild(QtWidgets.QListWidget, 'list_agenda').item(y_pos).data(self.DEFAULT_ITEM_ROLE)
        day_locale_text = StringValidator.LOCALE_DAY_OF_WEEK[self.DAY_OF_WEEK_KEY.index(item_data[0])]
        self.findChild(QtWidgets.QLabel, 'label_name').setText(item_data[1])
        self.findChild(QtWidgets.QLabel, 'label_day').setText(day_locale_text)
        self.findChild(QtWidgets.QLabel, 'label_time').setText(item_data[2] + ' WIB')
        self.findChild(QtWidgets.QLabel, 'label_place').setText(item_data[3])
        self.findChild(QtWidgets.QLabel, 'label_representative').setText(item_data[4])

    def on_day_selector_value_change(self):
        self.cur_day_int = self.findChild(QtWidgets.QTabWidget, 'day_selector').currentIndex()

        # Change the title appropriately.
        self.change_day_title()

        # Populate the QListWidget with the day's agenda.
        self.prefill_list_items()

    def on_dialog_agenda_accepted(self):
        # The input dialog's field data.
        name = self.d.findChild(QtWidgets.QLineEdit, 'field_name').text().strip()
        time = self.d.findChild(QtWidgets.QTimeEdit, 'event_time').time()
        place = self.d.findChild(QtWidgets.QLineEdit, 'field_place').text().strip()
        representative = self.d.findChild(QtWidgets.QLineEdit, 'field_representative').text().strip()

        # The "hidden" item order.
        order = int(self.d.findChild(QtWidgets.QLabel, 'app_title').toolTip())

        # Convert the time appropriately.
        time_h = self.zero_pad_time(time.hour())
        time_m = self.zero_pad_time(time.minute())
        time = time_h + ':' + time_m

        # The display title.
        display_text = f'{time} WIB --- {name}'

        if self.action == 'new':
            Lg('main.FrameAgenda.on_dialog_agenda_accepted', f'Creating a new agenda: {display_text} ...')

            # Append to the dict.
            self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].append({
                'name': name,
                'time': time,
                'place': place,
                'representative': representative
            })

            # Update the item's order.
            order = len(self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]]) - 1

            # Add a new item to the list.
            # Adding the list item.
            a = QtWidgets.QListWidgetItem()
            a.setData(
                self.DEFAULT_ITEM_ROLE,
                (self.DAY_OF_WEEK_KEY[self.cur_day_int], name, time, place, representative, order)
            )
            a.setText(display_text)
            self.findChild(QtWidgets.QListWidget, 'list_agenda').addItem(a)

            # Set the focus to the newly created item.
            self.findChild(QtWidgets.QListWidget, 'list_agenda').setCurrentItem(a)

        elif self.action == 'edit':
            Lg('main.FrameAgenda.on_dialog_agenda_accepted', f'Editing an existing agenda info: {display_text} ...')

            # The old data.
            old_item_data = self.cur_item.data(self.DEFAULT_ITEM_ROLE)
            old_day = old_item_data[0]
            old_name = old_item_data[1]
            old_time = old_item_data[2]
            old_place = old_item_data[3]
            old_representative = old_item_data[4]
            old_order = old_item_data[5]

            # Find the index of this item.
            idx = self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]].index({
                'name': old_name,
                'time': old_time,
                'place': old_place,
                'representative': old_representative
            })

            # Now we find the new index order of this item.
            order = idx

            # Edit the selected item's value.
            self.cur_item.setText(display_text)
            self.cur_item.setData(
                self.DEFAULT_ITEM_ROLE,
                (self.DAY_OF_WEEK_KEY[self.cur_day_int], name, time, place, representative, order)
            )

            # Now, edit the actual dict.
            self.agenda_dict[self.DAY_OF_WEEK_KEY[self.cur_day_int]][order] = {
                'name': name,
                'time': time,
                'place': place,
                'representative': representative
            }

        # Update the current selection and state.
        self.on_current_item_changed()

    def prefill_list_items(self):
        """
        Populate the QListWidget with the agenda list found in the GKI Salatiga+ JSON data.
        :return: nothing.
        """
        # Remove any selection.
        self.findChild(QtWidgets.QListWidget, 'list_agenda').clearSelection()

        # Remove any existing or previous item in the QListWidget.
        self.findChild(QtWidgets.QListWidget, 'list_agenda').clear()

        # Iterating through every list of existing forms in the agenda dict.
        the_day_key = self.DAY_OF_WEEK_KEY[self.cur_day_int]
        for a in self.agenda_dict[the_day_key]:
            # The current agenda's order in the dict.
            item_order = self.agenda_dict[the_day_key].index(a)

            # Adding the list item.
            b = QtWidgets.QListWidgetItem()
            b.setData(
                self.DEFAULT_ITEM_ROLE,
                (the_day_key, a['name'], a['time'], a['place'], a['representative'], item_order)
            )
            b.setText(f'{a["time"]} WIB --- {a["name"]}')
            self.findChild(QtWidgets.QListWidget, 'list_agenda').addItem(b)

        # Sort the list alphanumerically. [13]
        self.findChild(QtWidgets.QListWidget, 'list_agenda').setSortingEnabled(True)

    def zero_pad_time(self, time_int: int):
        if time_int < 10:
            return f'0{time_int}'
        else:
            return str(time_int)

    def call_action(self, action,
                    day: str = '',
                    name: str = '',
                    time: str = '',
                    place: str = '',
                    representative: str = '',
                    order: int = -1):
        """
        Determine what agenda action to take, as well as displaying the dialog.
        Possible values; 'new' and 'edit'.
        :param action: between 'new' and 'edit', specifies the agenda action to undergo.
        :param name: (optional) the current agenda's name.
        :param day: (optional) the current agenda's day.
        :param time: (optional) the current agenda's time.
        :param place: (optional) the current agenda's place.
        :param representative: (optional) the current agenda's representative.
        :param order: (optional) the current agenda's index in the agenda dict.
        :return: nothing.
        """
        self.action = action

        # Change the dialog's title according to the passed value.
        if action == 'new':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Tambahkan Agenda Mingguan Baru')

            # Clear the existing title and URL.
            self.d.findChild(QtWidgets.QLineEdit, 'field_name').setText('')
            self.d.findChild(QtWidgets.QLabel, 'field_day').setText(day)
            self.d.findChild(QtWidgets.QLineEdit, 'field_place').setText('')
            self.d.findChild(QtWidgets.QLineEdit, 'field_representative').setText('')
            self.d.findChild(QtWidgets.QTimeEdit, 'event_time').setTime(QTime(0, 0, 0, 0))

            # We store the index here.
            self.d.findChild(QtWidgets.QLabel, 'app_title').setToolTip(str(order))

        elif action == 'edit':
            self.d.findChild(QtWidgets.QLabel, 'app_title').setText('Edit Agenda Mingguan')

            # Preform the time to a QTime object.
            the_time_str = time.split(':')
            the_time = QTime(int(the_time_str[0]), int(the_time_str[1]), 0, 0)

            # Prefill with existing values.
            self.d.findChild(QtWidgets.QLineEdit, 'field_name').setText(name)
            self.d.findChild(QtWidgets.QLabel, 'field_day').setText(day)
            self.d.findChild(QtWidgets.QLineEdit, 'field_place').setText(place)
            self.d.findChild(QtWidgets.QLineEdit, 'field_representative').setText(representative)
            self.d.findChild(QtWidgets.QTimeEdit, 'event_time').setTime(the_time)

            # We store the index here.
            self.d.findChild(QtWidgets.QLabel, 'app_title').setToolTip(str(order))

        # Show the dialog.
        self.d.show()

        # Validate preliminary field values.
        self.d.validate_fields()
