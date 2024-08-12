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
    [3] Convert string to IO buffer
    - https://www.perplexity.ai/search/get-epoch-in-python-4SKpZJqIRpeWCVJqE6y9yQ
"""
import base64
import json
import os
import requests
import time

from lib.logger import Logger as Lg
from lib.preferences import SavedPreferences
from loading_animation import ScreenLoadingAnimation


class AppDatabase(object):

    GITHUB_JSON_FILENAME = 'gkisplus.json'
    GITHUB_JSON_URL = 'https://api.github.com/repos/gkisalatiga/gkisplus-data/contents/gkisplus.json'

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

        # Preamble logging.
        Lg('lib.database.AppDatabase.refresh_json_schema', f'Refreshing the local JSON schema ...')

        save_path = self.prefs.JSON_DATA_SCHEMA
        try:
            r = requests.get(self.GITHUB_JSON_URL)
            j = r.json()
            with open(save_path, 'w') as fo:
                fo.write(base64.b64decode(j['content']).decode('utf-8'))
            
            # Upon successful JSON data refresh, attempt to reload the JSON data again.
            self.load_json_schema()

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

    def push_json_schema(self, anim_window: ScreenLoadingAnimation = None, commit_msg: str = ''):
        """
        Push the local changes to the JSON schema into GKISalatiga+ GitHub repository
        where the data will be released and delivered to the GKISalatiga+ mobile app users.
        :param anim_window: the loading screen animator to prevent screen freezing during operations.
        :param commit_msg: the commit message.
        :return: push status, the generic GitHub API JSON response, and the log message.
        """
        commit_msg = f'Manual update from "Simon Petrus"' if commit_msg == '' else commit_msg

        try:
            # Retrieving the latest SHA in order to detect changes and checkpoints.
            msg = f'Retrieving the latest JSON schema\'s SHA checksum ...'
            Lg('lib.database.AppDatabase.push_json_schema', msg)
            anim_window.set_prog_msg(60, msg)
            r = requests.get(self.GITHUB_JSON_URL)
            latest_sha = r.json()['sha']

            # DEBUG. Please comment out on production.
            # print(r.json())

            # Merging the "meta" and "data" of the JSON schema.
            j = {
                'meta': self.db_meta,
                'data': self.db
            }
            j_as_json_string = json.dumps(j, ensure_ascii=False, indent=4)

            # DEBUG. Please comment out on production.
            # print(j_as_json_string)

            # Converting the current app's local JSON schema data into base64.
            b64_json_content = base64.b64encode(bytes(j_as_json_string, 'UTF-8')).decode('UTF-8')

            # Preparing the push request header and payload data.
            headers = {
                'Authorization': f'Bearer {self.credentials["api_github"]}',
                'Content-Type': 'application/json'
            }
            data_payload = {
                'message': commit_msg,
                'content': b64_json_content,
                'branch': 'main',
                'sha': latest_sha,
                'path': self.GITHUB_JSON_FILENAME
            }

            # Sending the http request.
            msg = f'Uploading the JSON data payload ...'
            anim_window.set_prog_msg(80, msg)
            Lg('lib.database.AppDatabase.push_json_schema', msg)
            # r = requests.put(self.GITHUB_JSON_URL, headers=headers, data=data_payload)
            r = requests.put(self.GITHUB_JSON_URL, headers=headers, json=data_payload)

            # DEBUG. Please comment out after use.
            # print(r.json())

            # Concluding logging.
            msg = f'Pushing GKI Salatiga+ app JSON data to main repository branch successful!'
            anim_window.set_prog_msg(100, msg)
            Lg('lib.database.AppDatabase.push_json_schema', msg)
            return True, r.json(), msg

        except Exception as e:
            msg = f'An unknown error has just happened: {e}'
            Lg('lib.database.AppDatabase.push_json_schema', msg)
            return False, {}, msg

    def save_local(self, updated_item: str = 'unspecified'):
        """
        Save the current state of the JSON schema into the local file.
        :param updated_item: the latest updated JSON item.
        :return: nothing.
        """
        with open(self.prefs.JSON_DATA_SCHEMA, 'w') as fo:
            # Preparing the JSON metadata.
            self.db_meta['update-count'] += 1
            self.db_meta['last-update'] = round(time.time())
            self.db_meta['last-actor'] = 'SIMON_PETRUS'
            self.db_meta['last-updated-item'] = updated_item

            # Prepare the dict to convert to JSON.
            a = {
                'meta': self.db_meta,
                'data': self.db
            }

            # Write/dump the JSON file.
            json.dump(a, fo, ensure_ascii=False, indent=4)
            Lg('lib.database.AppDatabase.save_local', f'Saved JSON schema successfully!')
