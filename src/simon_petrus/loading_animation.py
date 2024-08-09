"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import time

from ui import screen_loading_animation


class ScreenLoadingAnimation(QtWidgets.QMainWindow, screen_loading_animation.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenLoadingAnimation, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Displaying the animation GIF.
        gif = QtGui.QMovie('assets/loading_animation.gif')
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

        # This could probably mitigate the following error:
        # QBackingStore::endPaint() called with active painter;
        # did you forget to destroy it or call QPainter::end() on it?
        # ---
        # If problem persists, try removing the cache folder.
        time.sleep(0.001)

        self.set_status_message(msg)

    def set_progress(self, value: int):
        """
        Changes the progress bar value.
        :param value: the value of the progress bar to be displayed.
        :return: nothing.
        """
        val = 0 if value < 0 else value
        val = 100 if val > 100 else val
        self.findChild(QtWidgets.QProgressBar, 'main_progress').setValue(val)

    def set_status_message(self, msg: str):
        """
        Sets the message that will be displayed in the loading screen.
        :param msg: the message to display in the loading screen.
        :return: nothing.
        """
        self.findChild(QtWidgets.QLabel, 'label_status').setText(msg)
