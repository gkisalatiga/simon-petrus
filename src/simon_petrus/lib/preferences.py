"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from json.decoder import JSONDecodeError
import json
import os
# from pathlib import Path
import platformdirs as pfd
import shutil
import tempfile

from lib.exceptions import MalformedSettingsJSON
from lib.logger import Logger as Lg


class SavedPreferences(object):
    # The application identity.
    APP_NAME = 'simon_petrus'
    APP_AUTHOR = 'gkisalatiga'

    # The app's private local, app-specific directory.
    CONF_DIRECTORY = pfd.user_data_dir(APP_NAME, APP_AUTHOR)

    # The app's current session's temporary folder.
    TEMP_DIRECTORY = tempfile.mkdtemp(prefix='simon_petrus-')

    # Unescaped double backslash problem mitigation in Windows OS.
    if os.name == 'nt':
        CONF_DIRECTORY = CONF_DIRECTORY.replace('\\', '/')
        TEMP_DIRECTORY = TEMP_DIRECTORY.replace('\\', '/')

    # The app's settings JSON file.
    JSON_SETTINGS = CONF_DIRECTORY + os.sep + 'saved_preferences.json'

    # The GKI Salatiga+ downloaded (or fallback) JSON schema.
    JSON_DATA_SCHEMA = CONF_DIRECTORY + os.sep + 'data_schema.json'

    # The default settings/config template JSON structure.
    JSON_SETTINGS_TEMPLATE = {
        'autosync_on_launch': 1,
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

        # Don't forget to write the temporary settings into the JSON file.
        self.save_config()

    def init_configuration(self):
        """
        Initializes the config directory as well as ensuring that the config JSON
        is already created before proceeding with the app.
        :return: nothing.
        """

        # Ensuring that the config directory exists.
        try:
            os.makedirs(self.CONF_DIRECTORY, exist_ok=True)
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'User config folder created: {self.CONF_DIRECTORY}')
        except FileExistsError:
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'User config folder already exists: {self.CONF_DIRECTORY}')
        
        # Ensuring that the temporary directory exists.
        try:
            os.makedirs(self.TEMP_DIRECTORY, exist_ok=True)
            Lg('lib.preferences.SavedPreferences', f'Created the temporary directory: {self.TEMP_DIRECTORY}')
        except FileExistsError:
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'Temporary directory already exists: {self.CONF_DIRECTORY}')

        # Checking if the settings JSON file exists and is valid.
        try:
            with open(self.JSON_SETTINGS, 'r') as a:
                # Assigning the parsed JSON values into a Python dictionary.
                self.settings = json.load(a)

            # Testing if the loaded JSON file has the same set of keys.
            if not self.settings.keys() == self.JSON_SETTINGS_TEMPLATE.keys():
                raise MalformedSettingsJSON

        except JSONDecodeError:
            # If the JSON file is invalid, instead just recreate the JSON file from scratch.
            Lg('lib.preferences.SavedPreferences.init_config_dir',
                'Settings JSON file is invalid! Creating settings.json from scratch ...')
            self.create_default_config()

        except MalformedSettingsJSON:
            # If this clause is reached, we will attempt to upgrade/migrate the settings
            # instead of merely overwriting any previous settings with the default template.
            Lg('lib.preferences.SavedPreferences.init_config_dir',
               'Found non-conforming settings JSON file. Trying to migrate the settings ...')
            self.migrate_settings()

        except FileNotFoundError:
            # If the JSON file does not exist,
            # instead just recreate the JSON file from scratch.
            Lg('lib.preferences.SavedPreferences.init_config_dir',
                'Settings JSON file not found! Creating settings.json from scratch ...')
            self.create_default_config()

    def migrate_settings(self):
        """
        Given that a newer version of this app introduces new configuration items or categories,
        attempt to migrate the values in the previous config version into the newer one.
        :return: nothing.
        """
        with open(self.JSON_SETTINGS, 'r') as a:
            # Assigning the parsed JSON values into a temporary dictionary.
            old_settings = json.load(a)

            # Preparing the new, upgraded settings structure.
            new_settings = self.JSON_SETTINGS_TEMPLATE

            for item in old_settings.keys():
                new_settings[item] = old_settings[item]

            # Assigning the new, upgraded settings into the temporary file
            # and then save the settings into JSON file.
            self.settings = new_settings
            self.save_config()

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

        # Don't forget to write the temporary settings into the JSON file.
        self.save_config()
