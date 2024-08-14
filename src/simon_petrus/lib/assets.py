"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] Comparison of two files for similarities
    - https://docs.python.org/3/library/filecmp.html
    - https://stackoverflow.com/a/1072576
"""
import shutil
from zipfile import ZipFile
import base64
import filecmp
import os
import urllib.request

import requests

from lib.database import AppDatabase
from lib.logger import Logger as Lg
from lib.preferences import SavedPreferences
from loading_animation import ScreenLoadingAnimation


class AppAssets(object):
    """ Manages GKI Salatiga+ carousel, static HTML, and custom images data from the GitHub repo. """

    # The URL, path (relative to repo's root), and API end point of the main carousel data.
    CAROUSEL_ZIP_PATH = 'gkisplus-carousel.zip'
    CAROUSEL_ZIP_API = 'https://api.github.com/repos/gkisalatiga/gkisplus-data/contents/gkisplus-carousel.zip'
    CAROUSEL_ZIP_URL = 'https://raw.githubusercontent.com/gkisalatiga/gkisplus-data/main/gkisplus-carousel.zip'

    # The URL, path (relative to repo's root), and API end point of the main offertory QRIS image.
    QRIS_IMAGE_PATH = 'images/qris_gkis.png'
    QRIS_IMAGE_API = 'https://api.github.com/repos/gkisalatiga/gkisplus-data/contents/images/qris_gkis.png'
    QRIS_IMAGE_URL = 'https://raw.githubusercontent.com/gkisalatiga/gkisplus-data/main/images/qris_gkis.png'

    # The paths to primary assets section: carousel, static HTML, and custom images.
    ASSETS_PATH_CAROUSEL = 'carousel'
    ASSETS_PATH_IMAGES = 'images'
    ASSETS_PATH_STATIC = 'static'

    def __init__(self, global_pref: SavedPreferences, global_db: AppDatabase):
        self.credentials = global_db.credentials
        self.db = global_db.db
        self.db_meta = global_db.db_meta
        self.prefs = global_pref
        self.saved_carousel_loc = None
        self.saved_qris_loc = None

        # This determines whether to upload files.
        self.do_upload_carousel = False
        self.do_upload_main_qris = False

        # Initialize the assets folder before everything else.
        self.init_assets_folder()

    def init_assets_folder(self):
        """ Prepares the subfolders that will store the assets' data. """
        # Preamble logging.
        Lg('lib.assets.AppAssets.init_assets_folder', f'Initiating the assets folder ...')

        # Set the constants to also include the base folder prefix.
        self.ASSETS_PATH_CAROUSEL = self.prefs.ASSETS_DIRECTORY + os.sep + self.ASSETS_PATH_CAROUSEL
        self.ASSETS_PATH_IMAGES = self.prefs.ASSETS_DIRECTORY + os.sep + self.ASSETS_PATH_IMAGES
        self.ASSETS_PATH_STATIC = self.prefs.ASSETS_DIRECTORY + os.sep + self.ASSETS_PATH_STATIC

        # Unescaped double backslash problem mitigation in Windows OS.
        if os.name == 'nt':
            self.ASSETS_PATH_CAROUSEL = self.ASSETS_PATH_CAROUSEL.replace('\\', '/')
            self.ASSETS_PATH_IMAGES = self.ASSETS_PATH_IMAGES.replace('\\', '/')
            self.ASSETS_PATH_STATIC = self.ASSETS_PATH_STATIC.replace('\\', '/')

        # Ensures that these paths exist.
        try:
            os.makedirs(self.ASSETS_PATH_CAROUSEL, exist_ok=True)
        except FileExistsError:
            pass

        try:
            os.makedirs(self.ASSETS_PATH_IMAGES, exist_ok=True)
        except FileExistsError:
            pass

        try:
            os.makedirs(self.ASSETS_PATH_STATIC, exist_ok=True)
        except FileExistsError:
            pass

        # Init the carousel zip file location.
        self.saved_carousel_loc = self.ASSETS_PATH_CAROUSEL + os.sep + os.path.split(self.CAROUSEL_ZIP_URL)[1]

        # Post-logging.
        Lg('lib.assets.AppAssets.init_assets_folder', f'Initialization done!')

    def get_carousel(self, supress_download: bool = False, auto_extract: bool = True):
        """
        Download the GKI Salatiga+ main carousel Zip file from the GitHub repo.
        :param auto_extract: whether to automatically extract the zip file upon successful download.
        :param supress_download: whether to only return the downloaded path without actually downloading any zip file.
        :return: the local path to the downloaded carousel zip file.
        """
        download_url = self.CAROUSEL_ZIP_URL
        saved_file_path = self.saved_carousel_loc

        # Before all else, remove all files in the carousel extract directory in order to conserve space.
        shutil.rmtree(self.ASSETS_PATH_CAROUSEL, ignore_errors=True)
        os.makedirs(self.ASSETS_PATH_CAROUSEL, exist_ok=True)

        # Saving/downloading the zip file.
        if not supress_download:
            urllib.request.urlretrieve(download_url, saved_file_path)
            Lg('lib.assets.AppAssets.get_carousel', f'Successfully downloaded: {download_url}!')

        # Unzipping the data.
        if auto_extract:
            Lg('lib.assets.AppAssets.get_carousel', f'Extracting zip file: {saved_file_path}!')
            with ZipFile(saved_file_path, 'r') as z:
                z.extractall(self.ASSETS_PATH_CAROUSEL)

        # Return the carousel zip local path.
        return saved_file_path

    def get_main_qris(self, supress_download: bool = False):
        """
        Download the app's main QRIS code image for offertory from the GitHub source.
        :param supress_download: whether we should not re-download the QRIS image, but instead return its local path.
        :return: the local path to the downloaded QRIS image.
        """
        download_url = self.QRIS_IMAGE_URL
        saved_file_path = self.ASSETS_PATH_IMAGES + os.sep + os.path.split(download_url)[1]
        self.saved_qris_loc = saved_file_path

        # Saving/downloading the post image.
        if not supress_download:
            urllib.request.urlretrieve(download_url, saved_file_path)
            Lg('lib.assets.AppAssets.get_main_qris', f'Successfully downloaded: {download_url}!')

        # Return the main QRIS local path.
        return saved_file_path

    def push_assets(self, anim_window: ScreenLoadingAnimation = None):
        """
        Push all assets to the GitHub repo, with regard to file changes to save bandwith.
        :param anim_window: the loading screen animator to prevent screen freezing during operations.
        :return: push status, the generic GitHub API JSON response, and the log message.
        """

        try:
            # Uploading the QRIS image.
            if self.do_upload_main_qris:
                msg = f'Uploading the main QRIS image if there are changes ...'
                anim_window.set_prog_msg(10, msg)
                Lg('lib.assets.AppAssets.push_assets', msg)
                self.push_qris()

            # Uploading the carousel banners.
            if self.do_upload_carousel:
                msg = f'Uploading the carousel posters if there are changes ...'
                anim_window.set_prog_msg(20, msg)
                Lg('lib.assets.AppAssets.push_assets', msg)
                self.push_carousel()

            # Post-logging.
            msg = f'Data upload to the GitHub repo of GKI Salatiga+ successful!'
            Lg('lib.assets.AppAssets.push_assets', msg)
            return True, {}, msg

        except Exception as e:
            msg = f'An unknown error has just happened: {e}'
            Lg('lib.assets.AppAssets.push_assets', msg)
            return False, {}, msg

    def push_carousel(self):
        """
        Pushing the carousel banners.
        :return: nothing.
        """
        # Retrieving the latest SHA in order to detect changes and checkpoints.
        r = requests.get(self.CAROUSEL_ZIP_API)
        latest_sha = r.json()['sha']

        # DEBUG. Please comment out on production.
        # print(r.json())
        # print(self.db.keys())

        # DEBUG. Only for zipping.
        # ZipFile(self.saved_carousel_loc, mode='w', compression=8).write('/nadi/data/raw/downloads/maxresdefault.jpg')
        # print('Really None? ', z is None)
        # z.write('/nadi/data/raw/downloads/maxresdefault.jpg')
        # z.close()

        # Determining the location of the zip file.
        zip_loc = self.saved_carousel_loc

        # Zipping the carousel banners.
        with ZipFile(zip_loc, mode='w', compression=8) as zo:
            for a in self.db['carousel'].keys():
                # The current node.
                b = self.db['carousel'][a]

                # DEBUG.
                # print('Really None? ', zo is None)
                # print('WHY? ', zo, a)
                # zo.write('/nadi/data/raw/downloads/maxresdefault.jpg')
                # print('Really None? ', zo is None)

                base = self.ASSETS_PATH_CAROUSEL + os.sep + 'carousel' + os.sep + a
                zo.write(base + os.sep + b['banner'], arcname=('carousel' + os.sep + a + os.sep + b['banner']))

                # Only applies to posters.
                if b['type'] == 'poster':
                    zo.write(
                        base + os.sep + b['poster-image'],
                        arcname=('carousel' + os.sep + a + os.sep + b['poster-image'])
                    )

        # Read the zip file.
        with open(zip_loc, 'rb') as fi:
            carousel_bytes = fi.read()

        # Converting the zip file bytes into base64.
        carousel_b64_data = base64.b64encode(carousel_bytes).decode('UTF-8')

        # DEBUG. Please always comment out.
        # print(self.credentials)

        # Preparing the push request header and payload data.
        headers = {
            'Authorization': f'Bearer {self.credentials["api_github"]}',
            'Content-Type': 'application/json'
        }
        data_payload = {
            'message': 'Manual carousel update from "Simon Petrus"',
            'content': carousel_b64_data,
            'branch': 'main',
            'sha': latest_sha,
            'path': self.CAROUSEL_ZIP_PATH
        }

        # Sending the http request.
        msg = f'Uploading the carousel data payload ...'
        Lg('lib.assets.AppAssets.push_carousel', msg)
        r = requests.put(self.CAROUSEL_ZIP_API, headers=headers, json=data_payload)

        # DEBUG. Please comment out after use.
        # print(r.json())

        # Concluding logging.
        msg = f'Pushing GKI Salatiga+ app carousel zip file to main repository branch successful!'
        Lg('lib.database.AppDatabase.push_carousel', msg)

    def push_qris(self):
        """
        Pushing the QRIS image.
        :return: nothing.
        """
        # Retrieving the latest SHA in order to detect changes and checkpoints.
        r = requests.get(self.QRIS_IMAGE_API)
        latest_sha = r.json()['sha']

        # DEBUG. Please comment out on production.
        # print(r.json())

        # Read the image file.
        with open(self.saved_qris_loc, 'rb') as fi:
            qris_bytes = fi.read()

        # Converting the QRIS image bytes into base64.
        qris_b64_data = base64.b64encode(qris_bytes).decode('UTF-8')

        # DEBUG. Please always comment out.
        # print(self.credentials)

        # Preparing the push request header and payload data.
        headers = {
            'Authorization': f'Bearer {self.credentials["api_github"]}',
            'Content-Type': 'application/json'
        }
        data_payload = {
            'message': 'Manual QRIS update from "Simon Petrus"',
            'content': qris_b64_data,
            'branch': 'main',
            'sha': latest_sha,
            'path': self.QRIS_IMAGE_PATH
        }

        # Sending the http request.
        msg = f'Uploading the QRIS data payload ...'
        Lg('lib.assets.AppAssets.push_qris', msg)
        r = requests.put(self.QRIS_IMAGE_API, headers=headers, json=data_payload)

        # DEBUG. Please comment out after use.
        # print(r.json())

        # Concluding logging.
        msg = f'Pushing GKI Salatiga+ app QRIS image to main repository branch successful!'
        Lg('lib.database.AppDatabase.push_qris', msg)

    def queue_main_qris_change(self, new_qris_path: str):
        """
        Queue to change the QRIS image with a newer one as well as detecting changes between old and new QRIS images,
        so that if the user does not change the image, the bandwith is not used.
        :param new_qris_path: the path to the QRIS path that will replace the existing one.
        :return: nothing.
        """
        # Comparing the two bytes. [1]
        if not filecmp.cmp(self.saved_qris_loc, new_qris_path):
            self.do_upload_main_qris = True

            # Debug logging.
            Lg('lib.assets.AppAssets.queue_main_qris_change', 'QRIS image difference found! Overwriting ...')

            # Since the two files are not the same,
            # we will thus overwrite the old image with the new one.
            with open(new_qris_path, 'rb') as fi:
                new_img_bytes = fi.read()
            with open(self.saved_qris_loc, 'wb') as fo:
                fo.write(new_img_bytes)

        else:
            Lg('lib.assets.AppAssets.queue_main_qris_change', 'Nothing interesting down here.')
            self.do_upload_main_qris = False

    def set_credentials(self, cred: dict):
        self.credentials = cred
