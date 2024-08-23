"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""
from urllib.error import URLError
import urllib

from PyQt5 import QtWidgets

from lib.logger import Logger as Lg
from lib.assets import AppAssets
from lib.database import AppDatabase
from lib.preferences import SavedPreferences
from loading_animation import ScreenLoadingAnimation

# ------------------------ THIS SECTION DEALS WITH THE GLOBAL VARIABLES ------------------------ #

global anim
global app_assets
global app_db
global cur_fragment
global prefs
global win_main


def init():
    # The app-wide application preferences.
    # Initializes the app's internally saved preferences (global variable).
    global prefs
    prefs = SavedPreferences()
    prefs.init_configuration()

    # Initializes the app's internal database (global variable).
    global app_db
    app_db = AppDatabase()

    # Initializes the app's assets manager.
    global app_assets
    app_assets = AppAssets()

    # The global loading screen animator.
    global anim
    anim = ScreenLoadingAnimation()

    # The main and primary window of the app.
    global win_main

    # The active fragment in the main screen's (win_main's) main frame.
    # Determining the default fragment to show at startup.
    global cur_fragment
    cur_fragment = 'fragment_default'


# ------------------------ THIS SECTION DEALS WITH THE STATIC FUNCTIONS ------------------------ #
# ------------------------------- MIGRATED FROM "main.py" -------------------------------------- #


# DEBUG: For testing variable change and remembered states.
debug_int_value = 0


def disable_widget(qt_widget: QtWidgets.QWidget):
    """
    This function will disable all elements inside a given QtWidget, including the widget itself.
    :param qt_widget: the QWidget whose children will be disabled.
    :return: nothing.
    """
    qt_widget.setEnabled(False)


def enable_widget(qt_widget: QtWidgets.QWidget):
    """
    This function will enable all elements inside a given QtWidget, including the widget itself.
    :param qt_widget: the QWidget whose children will be enabled.
    :return: nothing.
    """
    qt_widget.setEnabled(True)


def push_all_data():
    """
    This function pushes the JSON schemas as well as the individual carousel, static HTML,
    and custom images data.
    :return: the "app_db.push_json_schema"'s return value, anything it is.
    """
    # Ensures the latest temporary JSON dict is retrieved.
    app_assets.db = app_db.db

    # Round one: uploading the assets data.
    is_success, j_1, msg = app_assets.push_assets(anim)
    if not is_success:
        return is_success, j_1, msg

    # Round two: uploading the JSON schema.
    is_success, j_2, msg = app_db.push_json_schema(anim)
    if not is_success:
        return is_success, j_2, msg

    # Final return: if successful.
    msg = 'All assets data and JSON schema have been uploaded and committed successfully!'
    return True, (j_1, j_2), msg


def refresh_all_data():
    """
    This function refreshes all data used in this app, from the main JSON schema
    to the carousel, custom images, and static HTML.
    :return: True (not significant, but it is expressed so that the multithreader won't freeze infinitely).
    """
    try:
        app_db.refresh_json_schema()
        app_assets.get_carousel()
        app_assets.get_gallery()
        app_assets.get_static()
        app_assets.get_main_qris()
        return True, 'Data synchronization successful!'

    except URLError as e:
        msg = f'Error encountered while refreshing all data. The internet suddenly disconnects: {e}'
        Lg('global_schema.refresh_all_data', msg)
        return False, msg

    except Exception as e:
        msg = f'Unknown error encountered: {e}'
        Lg('global_schema.refresh_all_data', msg)
        return False, msg
