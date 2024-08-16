"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets
import sys

from handler.screen.screen_credential_decrypt import ScreenCredentialDecrypt
import global_schema

if __name__ == '__main__':
    # Initiating and constructing the QApplication.
    app = QtWidgets.QApplication(sys.argv)

    # Initializing the app-wide global variable. [15]
    global_schema.init()

    # Establishing the main window that gets shown on start up.
    # win = ScreenTest()  # --- debug only. uncomment if not needed.
    win = ScreenCredentialDecrypt()
    win.show()

    # Actually exiting the app.
    exit_code = app.exec()

    # Performing post-operation procedures.
    global_schema.prefs.shutdown()

    # Appropriately exiting the app.
    sys.exit(exit_code)
