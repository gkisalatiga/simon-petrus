"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] Use slots and signals to update the progress bar value to avoid segmentation fault
    - https://stackoverflow.com/a/50105605
    [2] Covert GIF to base64, and displaying base64 in PyQt5
    - https://www.perplexity.ai/search/python-convert-gif-to-base64-6ZLLwiVERFOsLzrVBuqvIw
"""
import base64

from PyQt5 import QtCore, QtGui, QtWidgets
import time

from PyQt5.QtCore import pyqtSignal, QBuffer, QByteArray

from lib.external.meipass import resource_path
from ui import screen_loading_animation


class ScreenLoadingAnimation(QtWidgets.QMainWindow, screen_loading_animation.Ui_MainWindow):

    # The signal for updating the progress bar value. [1]
    sig_loading_progress = pyqtSignal(int)

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenLoadingAnimation, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Connecting the slot for updating the progress bar value.
        self.sig_loading_progress.connect(self.main_progress.setValue)

        # Decode the base64 GIF buffer.
        # gif_data = base64.b64decode(assets.loading_animation.value)
        # buffer = QBuffer()
        # buffer.setData(QByteArray(gif_data))
        # buffer.open(QBuffer.ReadOnly)

        # Displaying the animation GIF from GIF base64 buffer. [2]
        # gif = QtGui.QMovie(buffer)
        # self.label_gif.setMovie(gif)
        # gif.start()
        gif = QtGui.QMovie(resource_path('assets/loading_animation.gif'))
        self.label_gif.setMovie(gif)
        gif.start()


    def reset_prog_msg(self):
        """
        Resetting the progress bar value and the status message.
        :return: nothing.
        """
        self.set_prog_msg(0, '')

    def clear_and_show(self):
        """
        Clears the current progress bar value and status message, then display this window.
        :return:
        """
        self.show()
        self.reset_prog_msg()

    def set_prog_msg(self, value: int, msg: str):
        """
        Changes both the progress bar progression as well as the status message.
        :param value: the value of the progress bar to be displayed.
        :param msg: the message to display in the loading screen.
        :return: nothing.
        """
        self.set_progress(value)

        # DEBUG: Please comment out this block upon production.
        # ---
        # This could probably mitigate the following error:
        # QBackingStore::endPaint() called with active painter;
        # did you forget to destroy it or call QPainter::end() on it?
        # Segmentation fault (core dumped)
        # ---
        # If problem persists, try removing the cache folder.
        # print('Does "segmentation fault" persist at this block?')
        time.sleep(0.001)

        self.set_status_message(msg)

        # DEBUG: Please comment out this block upon production.
        # print('Nothing awry happened.')

    def set_progress(self, value: int):
        """
        Changes the progress bar value.
        :param value: the value of the progress bar to be displayed.
        :return: nothing.
        """
        val = 0 if value < 0 else value
        val = 100 if val > 100 else val

        # DEBUG: Always comment out on production.
        # print('Is this progress bar causing the problem? Let\'s see...')

        self.sig_loading_progress.emit(val)
        # self.main_progress.setValue(val)
        # self.findChild(QtWidgets.QProgressBar, 'main_progress').setValue(val)

        # DEBUG: Always comment out on production.
        # print('Nope.')

    def set_status_message(self, msg: str):
        """
        Sets the message that will be displayed in the loading screen.
        :param msg: the message to display in the loading screen.
        :return: nothing.
        """
        self.findChild(QtWidgets.QLabel, 'label_status').setText(msg)
