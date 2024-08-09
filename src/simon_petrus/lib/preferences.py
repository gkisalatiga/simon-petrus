"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from json.decoder import JSONDecodeError
import json
import os
import platformdirs as pfd
import shutil
import tempfile

from lib.logger import Logger as Lg


class SavedPreferences(object):
    # The application identity.
    APP_NAME = 'simon_petrus'
    APP_AUTHOR = 'gkisalatiga'

    # The app's private local, app-specific directory.
    CONF_DIRECTORY = pfd.user_data_dir(APP_NAME, APP_AUTHOR)

    # The app's current session's temporary folder.
    TEMP_DIRECTORY = tempfile.mkdtemp(prefix='simon_petrus-')
    Lg('lib.preferences.SavedPreferences', f'Created the temporary directory: {TEMP_DIRECTORY}')

    # The app's settings JSON file.
    JSON_SETTINGS = CONF_DIRECTORY + os.sep + 'saved_preferences.json'

    # The GKI Salatiga+ downloaded (or fallback) JSON schema.
    JSON_DATA_SCHEMA = CONF_DIRECTORY + os.sep + 'data_schema.json'

    # The default settings/config template JSON structure.
    JSON_SETTINGS_TEMPLATE = {
        'remember_cred_loc': 0,
        'saved_cred_loc': '',
    }

    def __init__(self):
        self.settings = {}
        pass

    def create_default_config(self):
        """
        Initializes the default (empty) settings JSON file.
        Calling this function will overwrite the previous settings file.
        :return: nothing.
        """
        with open(self.JSON_SETTINGS, 'w') as a:
            a.write(json.dumps(self.JSON_SETTINGS_TEMPLATE))
            self.settings = self.JSON_SETTINGS_TEMPLATE

    def init_configuration(self):
        """
        Initializes the config directory as well as ensuring that the config JSON
        is already created before proceeding with the app.
        :return: nothing.
        """

        # Ensuring that the config directory exists.
        try:
            os.mkdir(self.CONF_DIRECTORY)
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'User config folder created: {self.CONF_DIRECTORY}')
        except FileExistsError:
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'User config folder already exists: {self.CONF_DIRECTORY}')

        # Checking if the settings JSON file exists and is valid.
        try:
            with open(self.JSON_SETTINGS, 'r') as a:
                # Assigning the parsed JSON values into a Python dictionary.
                self.settings = json.load(a)

            # Testing if the loaded JSON file has the same set of keys.
            if not self.settings.keys() == self.JSON_SETTINGS_TEMPLATE.keys():
                raise JSONDecodeError

        except JSONDecodeError:
            # If the JSON file is invalid, instead just recreate the JSON file from scratch.
            Lg('lib.preferences.SavedPreferences.init_config_dir',
                'Settings JSON file is invalid! Creating settings.json from scratch ...')
            self.create_default_config()

        except FileNotFoundError:
            # If the JSON file does not exist,
            # instead just recreate the JSON file from scratch.
            Lg('lib.preferences.SavedPreferences.init_config_dir',
                'Settings JSON file not found! Creating settings.json from scratch ...')
            self.create_default_config()

    def save_config(self):
        """
        Writing the app's temporary settings dict into a permanent JSON file
        in an external storage.
        :return: nothing.
        """
        with open(self.JSON_SETTINGS, 'w') as a:
            Lg('lib.preferences.SavedPreferences.save_config', 'Exporting settings right now ...')
            a.write(json.dumps(self.settings))

    def shutdown(self):
        """
        Appropriately and properly close the app by performing post-open procedures,
        such as removing the temporary directory.
        :return: nothing.
        """
        # Removing the temporary directory in order to conserve space.
        if os.path.isdir(self.TEMP_DIRECTORY):
            Lg('lib.preferences.SavedPreferences.shutdown', f'Removing the temporary directory ...')
            shutil.rmtree(self.TEMP_DIRECTORY)
