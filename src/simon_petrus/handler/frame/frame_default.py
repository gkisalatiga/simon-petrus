"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets

from ui import frame_default


class FrameDefault(QtWidgets.QFrame, frame_default.Ui_Frame):
    def __init__(self, *args, obj=None, **kwargs):
        super(FrameDefault, self).__init__(*args, **kwargs)
        self.setupUi(self)
