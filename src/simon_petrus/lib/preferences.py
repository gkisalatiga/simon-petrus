"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from json.decoder import JSONDecodeError
import json
import os
from pathlib import Path

import platformdirs as pfd
import shutil
import tempfile

from PyQt5 import QtCore

import global_schema
from lib.credentials import CredentialGenerator
from lib.exceptions import MalformedSettingsJSON
from lib.external.thread import ThreadWithResult
from lib.logger import Logger as Lg


class SavedPreferences(object):
    # The application identity.
    APP_NAME = 'simon_petrus'
    APP_AUTHOR = 'gkisalatiga'

    # The app's private local, app-specific directory.
    CONF_DIRECTORY = pfd.user_data_dir(APP_NAME, APP_AUTHOR)

    # The app's current session's temporary folder.
    TEMP_DIRECTORY = tempfile.mkdtemp(prefix='simon_petrus-')

    # The GKI Salatiga+ asset data folder.
    ASSETS_DIRECTORY = CONF_DIRECTORY + os.sep + 'assets'

    # Unescaped double backslash problem mitigation in Windows OS.
    if os.name == 'nt':
        CONF_DIRECTORY = CONF_DIRECTORY.replace('\\', '/')
        TEMP_DIRECTORY = TEMP_DIRECTORY.replace('\\', '/')
        ASSETS_DIRECTORY = ASSETS_DIRECTORY.replace('\\', '/')

    # The app's settings JSON file.
    JSON_SETTINGS = CONF_DIRECTORY + os.sep + 'saved_preferences.json'

    # The GKI Salatiga+ downloaded (or fallback) JSON schema.
    JSON_DATA_SCHEMA = CONF_DIRECTORY + os.sep + 'data_schema.json'

    # The temporarily stored Google OAUTH2.0 token.
    JSON_GOOGLE_ACCOUNT_SERVICE_KEY = TEMP_DIRECTORY + os.sep + 'temp_oauth_token_refresh.json'

    # The default settings/config template JSON structure.
    JSON_SETTINGS_TEMPLATE = {
        'autosync_on_launch': 1,
        'gdrive_fetch_all_photos': 0,
        'remember_cred_loc': 0,
        'saved_cred_loc': '',
    }

    def __init__(self):
        self.settings = {}
        self.session_json_enc_path = ''
        self.session_secret = ''
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

        # Ensuring that the assets directory exists.
        try:
            os.makedirs(self.ASSETS_DIRECTORY, exist_ok=True)
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'Assets directory created: {self.ASSETS_DIRECTORY}')
        except FileExistsError:
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'Assets folder already exists: {self.ASSETS_DIRECTORY}')

        # DEBUG. Why can't the temporary folder be created?
        # _0x123 = '/tmp/0x123'
        # print(f"Is exists?: {os.path.exists(self.TEMP_DIRECTORY)}")
        # print(f"Creating: {_0x123}")
        # Path(_0x123).mkdir(exist_ok=True, parents=True)
        # print(f"{_0x123} Done.")

        # Ensuring that the temporary directory exists.
        Path(self.TEMP_DIRECTORY).mkdir(exist_ok=True, parents=True)
        try:
            os.makedirs(self.TEMP_DIRECTORY, exist_ok=True)
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'Created the temporary directory: {self.TEMP_DIRECTORY}')
        except FileExistsError:
            Lg('lib.preferences.SavedPreferences.init_config_dir', f'Temporary directory already exists: {self.TEMP_DIRECTORY}')

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
        # DEBUG.
        # print(self.session_json_enc_path)
        # print(self.session_secret)
        # print(self.JSON_GOOGLE_OAUTH_TOKEN)

        # Saving the latest generated Google Drive OAUTH token to the encrypted JSON location.
        if os.path.isfile(self.session_json_enc_path) and os.path.isfile(self.JSON_GOOGLE_ACCOUNT_SERVICE_KEY):
            Lg('lib.preferences.SavedPreferences.shutdown', f'Overwriting old and expired Google OAUTH tokens ...')

            # The current session's loaded credential.
            a = global_schema.app_db.credentials

            # Converting the OAUTH2.0 JSON file into a Python dict.
            with open(self.JSON_GOOGLE_ACCOUNT_SERVICE_KEY, 'r') as b:
                a['authorized_drive_oauth'] = json.load(b)

            # Now encrypt the JSON data.
            generator = CredentialGenerator()

            # Encrypt the credential.
            encrypted_bytes = generator.encrypt(a, self.session_secret)

            # Save the file.
            with open(self.session_json_enc_path, 'wb') as fo:
                fo.write(encrypted_bytes)

        else:
            Lg(
                'lib.preferences.SavedPreferences.shutdown',
                f'It\'s weird! Why doesn\'t the Google API OAUTH2.0 token refresher get updated?'
            )

        # Removing the temporary directory in order to conserve space and maximize security.
        if os.path.isdir(self.TEMP_DIRECTORY):
            Lg('lib.preferences.SavedPreferences.shutdown', f'Removing the temporary directory ...')
            shutil.rmtree(self.TEMP_DIRECTORY)

        # Don't forget to write the temporary settings into the JSON file.
        self.save_config()
