"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from lib.logger import Logger as Lg
from ui import screen_test


class ScreenTest(QtWidgets.QMainWindow, screen_test.Ui_MainWindow):
    """ Used during development to try out new features and debug app's code. """

    def __init__(self, *args, obj=None, **kwargs):
        super(ScreenTest, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Preamble logging.
        Lg('main.ScreenTest', '[DEBUG] Initiating the debug ScreenTest window ...')

        # Which test method to run?
        # (Uncomment the ones not needed.)
        # self.test_001()

    def test_001(self):
        """ Displaying image using QPixmap. [12] """
        pixmap = QPixmap('assets/test_image.png')
        self.label_test.setPixmap(pixmap)
