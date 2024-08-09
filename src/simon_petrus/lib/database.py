"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] AES encryption of strings
    - https://onboardbase.com/blog/aes-encryption-decryption
    [2] Download remote file from the internet and save as a local file
    - https://www.perplexity.ai/search/how-to-write-bytes-to-external-BR51zzfoTqW2JcFmV4xQtg
"""
import base64
import json
import os
import requests

from lib.logger import Logger as Lg
from lib.preferences import SavedPreferences


class AppDatabase(object):
    GITHUB_JSON_PULL_URL = 'https://api.github.com/repos/gkisalatiga/gkisplus-data/contents/gkisplus.json'

    def __init__(self, global_pref: SavedPreferences):
        self.credentials = {}
        self.db = {}
        self.db_meta = {}
        self.is_db_exist = False
        self.is_db_valid = False
        self.prefs = global_pref

    def load_json_schema(self):
        """
        If exists in the app's directory, parse the downloaded JSON schema as dict
        and then save the dict as this class' property.
        :return: nothing.
        """
        json_loc = self.prefs.JSON_DATA_SCHEMA
        if os.path.isfile(json_loc):
            self.is_db_exist = True
            with open(json_loc, 'r') as fi:
                try:
                    parsed_json = json.load(fi)
                    self.db = parsed_json['data']
                    self.db_meta = parsed_json['meta']
                    self.is_db_valid = True
                    Lg('lib.database.AppDatabase.load_json_schema',
                       f'Loaded cached JSON schema: {json_loc}')
                except Exception as e:
                    self.db = {}
                    self.is_db_valid = False
                    Lg('lib.database.AppDatabase.load_json_schema',
                       f'Cannot parse {json_loc}. Error when validating the JSON schema: {e}')
        else:
            self.is_db_exist = False
            self.is_db_valid = False

            # Fallback. Retrieve the latest JSON data if the local one is corrupt.
            self.refresh_json_schema()

    def refresh_json_schema(self):
        """
        Downloads the GKI Salatiga+ JSON schema from the remote source (GitHub repo).
        :return: True if download is successful.
        """
        save_path = self.prefs.JSON_DATA_SCHEMA
        try:
            r = requests.get(self.GITHUB_JSON_PULL_URL)
            j = r.json()
            with open(save_path, 'w') as fo:
                fo.write(base64.b64decode(j['content']).decode('utf-8'))

            return True
        except Exception as e:
            Lg('lib.database.AppDatabase.refresh_json_schema', f'Exception encountered: {e}')
            return False

    def populate_credentials(self, creds: dict):
        """
        Populate the app's database with API keys and OAUTH2.0 tokens that will be used
        to read, update, and create the app's cloud data.
        :param creds: the API key and OAUTH2.0 token credentials that will be used to retrieve the DB.
        :return: nothing.
        """
        self.credentials = creds

    def save_local(self):
        """
        Save the current state of the JSON schema into the local file.
        :return: nothing.
        """
        with open(self.prefs.JSON_DATA_SCHEMA, 'w') as fo:
            # Prepare the dict to convert to JSON.
            a = {
                'meta': self.db_meta,
                'data': self.db
            }

            # Write/dump the JSON file.
            json.dump(a, fo)
            Lg('lib.database.AppDatabase.save_local', f'Saved JSON schema successfully!')
