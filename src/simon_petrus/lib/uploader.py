"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] WordPress REST API references
    - https://medium.com/@vicgupta/how-to-upload-a-post-or-image-to-wordpress-using-rest-api-220fe046ff7a
    [2] Detecting the mime type of a file
    - https://stackoverflow.com/a/2753385
    [3] Generating PDF thumbnail preview from a PDF file
    - https://gist.github.com/alamsal/bdfa7528cc9bd291e527
    - https://www.perplexity.ai/search/python-how-to-extract-pdf-thum-TMFKWhPuQRq_NwmuB6zL9A
    [4] Uploading files to Google Drive using the Google Drive API
    - https://developers.google.com/drive/api/quickstart/python#configure_the_sample
    [5] Uploading media, posts, and pages to the WordPress REST API
    - https://medium.com/@vicgupta/how-to-upload-a-post-or-image-to-wordpress-using-rest-api-220fe046ff7a
    - https://www.perplexity.ai/search/how-to-enable-wordpress-rest-a-LpkHRItmQTONiPsqf_.rsw
    [6] Backtracing in Python
    - https://www.perplexity.ai/search/python-how-to-backtrace-error-RSgsVAVwRhuuQ2skpNfR_g
    [7] Scraping the latest Instagram post
    - https://pypi.org/project/instascrap
    [8] Parsing query parameters from a URL
    - https://www.perplexity.ai/search/how-to-parse-url-parameter-in-WSLXEUNZTdedJpXCr7cVKA
"""

from datetime import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from instascrap import InstaScraper
from urllib.parse import urlparse, parse_qs
import fitz
import json
import os
import requests
import traceback
import urllib.request

from lib.database import AppDatabase
from lib.exceptions import InvalidMimeTypeException, UploadFileSizeTooBig, MalformedHttpResponseJSON
from lib.logger import Dumper as Dmp
from lib.logger import Logger as Lg
from lib.mimetypes import MimeTypes
from lib.preferences import SavedPreferences
from loading_animation import ScreenLoadingAnimation


class Uploader(object):

    # The Google Drive API scopes.
    GOOGLE_DRIVE_SCOPES = [
        'https://www.googleapis.com/auth/docs',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.apps.readonly',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.meet.readonly',
        'https://www.googleapis.com/auth/drive.metadata',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.photos.readonly',
        'https://www.googleapis.com/auth/drive.readonly',
    ]

    # The Google Drive ID of "Warta Jemaat" uploads.
    GDRIVE_ID_WARTA_JEMAAT = '1Nof_4RXb6RY33lkv__5uw4q3v5Ogf9oc'

    # The Google Drive ID of "Tata Ibadah" uploads.
    GDRIVE_ID_LITURGI = '1s4Zm9-FSMjr2kNeJ-f3AS5imlpOQl5yT'

    # Instagram account name of GKI Salatiga.
    IG_ACCOUNT_USERNAME = 'gkisalatiga'

    # The WordPress domain target.
    WP_DOMAIN_TARGET = 'https://gkisalatiga.org'

    # The WordPress REST API endpoint for uploading media.
    WP_ENDPOINT_MEDIA = f'{WP_DOMAIN_TARGET}/wp-json/wp/v2/media'

    # The WordPress REST API endpoint for uploading pages.
    WP_ENDPOINT_PAGES = f'{WP_DOMAIN_TARGET}/wp-json/wp/v2/pages'

    # The WordPress REST API endpoint for uploading posts.
    WP_ENDPOINT_POSTS = f'{WP_DOMAIN_TARGET}/wp-json/wp/v2/posts'

    # The category REST API for WordPress of GKISalatiga.org.
    WP_ENDPOINT_CATEGORY = f'{WP_DOMAIN_TARGET}/wp-json/wp/v2/categories'

    # The YouTube embed prefix.
    YT_EMBED_PREFIX = 'https://www.youtube.com/embed'

    # API endpoint for retrieving playlist data in YouTube.
    YT_ENDPOINT_PLAYLIST_ITEMS = 'https://www.googleapis.com/youtube/v3/playlistItems'

    # API endpoint for retrieving video data in YouTube.
    YT_ENDPOINT_VIDEO_ITEMS = 'https://www.googleapis.com/youtube/v3/videos'

    # The "Kebaktian Umum" playlist ID of GKI Salatiga.
    YT_PLAYLIST_KEBAKTIAN_UMUM = 'PLtAv1OZRTdvI1P3YIJ4_qOqapZjV1PtnI'

    def __init__(
            self, anim_window: ScreenLoadingAnimation = None,
            global_pref: SavedPreferences = None,
            global_db: AppDatabase = None
    ):
        self.anim = anim_window
        self.prefs = global_pref
        self.app_db = global_db

    def edit_wp_post(self, post_id: int, new_content: str):
        """
        Edit and update an existing WordPress post in GKISalatiga.org. [5]
        :param post_id: the post ID of the post that will be edited.
        :param new_content: the new content that will overwrite the previous post content.
        :return: generic WordPress REST API JSON dict response.
        """
        with requests.Session() as s:
            # Prepare the request header.
            wp_token = self.app_db.credentials['wp_authorization']
            header = {'Authorization': 'Basic ' + wp_token}

            # Finding the post ID's corresponding post URL.
            post_url = self.WP_ENDPOINT_PAGES + '/' + str(post_id)

            # Updating the post.
            post_data = {'content': new_content}
            r = s.post(post_url, headers=header, json=post_data)

        # Return the obtained data.
        return r.json()

    def generate_pdf_thumbnail(self, pdf_path: str):
        """
        Generate PDF overview thumbnail as an image.
        :param pdf_path: the string pointing to the respective PDF file's path.
        :return: the generated thumbnail's image path.
        """

        # Determining the output filename.
        filename_without_extension = os.path.splitext(os.path.split(pdf_path)[1])[0]
        output_file = self.prefs.TEMP_DIRECTORY + os.sep + filename_without_extension + '.png'

        # Setting PDF thumbnail image quality.
        dpi = 75
        zoom_factor = dpi / 72

        # Generating the rasterization of PDF using PyMuPDF (fitz).
        magnify = fitz.Matrix(zoom_factor, zoom_factor)
        raster_doc = fitz.open(pdf_path)

        # Saving only the raster image of the first page of the PDF only.
        pix = raster_doc[0].get_pixmap(matrix=magnify)
        pix.save(output_file)

        # Returning the output thumbnail path.
        return output_file

    def get_latest_ig_post(self, account_name: str):
        """
        Retrieve one and only one last post of an Instagram account.
        This function also downloads the image of the post.
        :param account_name: the account name to scrape for the latest post.
        :return: the path of the downloaded latest Instagram post picture, as well as its metadata.
        """
        ig_s = InstaScraper()

        # Scrape the Instagram post data. [7]
        r = ig_s.Scraper({'usernames': [account_name]})[0]

        # Preparing the latest post's metadata
        meta = r['latestPosts'][0]

        # Saving/downloading the post image.
        download_url = meta['displayUrl']
        saved_file_path = self.prefs.TEMP_DIRECTORY + os.sep + 'ig_post-' + meta['id'] + '.webp'
        urllib.request.urlretrieve(download_url, saved_file_path)

        # Return the desired response data.
        return saved_file_path, meta

    def get_latest_liturgi(self):
        """
        Scrape 10 the latest tata ibadah posts uploaded to GKISalatiga.org.
        :return: a standard dict specifying the latest tata ibadah data, as returned by the WordPress REST API.
        """
        with requests.Session() as s:
            s.get(self.WP_DOMAIN_TARGET)

            # The authorization header.
            wp_token = self.app_db.credentials['wp_authorization']
            header = {'Authorization': 'Basic ' + wp_token}

            # Retrieving the category ID.
            cat_slug = 'tata-ibadah'
            r = s.get(self.WP_ENDPOINT_CATEGORY + f'?slug={cat_slug}', headers=header)

            # The category ID:
            category_id = r.json()[0]['id']
            Lg('lib.uploader.Uploader.get_latest_liturgi', f'Category "{cat_slug}" has the following ID: {category_id}')

            # Fetch the latest category posts.
            r = s.get(self.WP_ENDPOINT_POSTS + f'?categories={category_id}', headers=header)

        return r.json()

    def get_latest_warta(self):
        """
        Scrape 10 the latest warta jemaat posts uploaded to GKISalatiga.org.
        :return: a standard dict specifying the latest warta jemaat data, as returned by the WordPress REST API.
        """
        with requests.Session() as s:
            s.get(self.WP_DOMAIN_TARGET)

            # The authorization header.
            wp_token = self.app_db.credentials['wp_authorization']
            header = {'Authorization': 'Basic ' + wp_token}

            # Retrieving the category ID.
            cat_slug = 'warta-jemaat'
            r = s.get(self.WP_ENDPOINT_CATEGORY + f'?slug={cat_slug}', headers=header)

            # The category ID:
            category_id = r.json()[0]['id']
            Lg('lib.uploader.Uploader.get_latest_warta', f'Category "{cat_slug}" has the following ID: {category_id}')

            # Fetch the latest category posts.
            r = s.get(self.WP_ENDPOINT_POSTS + f'?categories={category_id}', headers=header)

        # Return the data.
        return r.json()

    def get_latest_yt_playlist(self, playlist_id):
        """
        Retrieve the last 50 snippet data of a given YouTube playlist.
        :param playlist_id: the playlist ID whose data will be fetched.
        :return: a generic YouTube API v3 JSON dict.
        """
        # Prepare the YouTube API v3 API key.
        key = self.app_db.credentials['api_youtube']

        # Preparing the request queries.
        part = 'snippet'
        max_results = 50

        # Fetching the data.
        with requests.Session() as s:
            r = s.get(self.YT_ENDPOINT_PLAYLIST_ITEMS + f'?key={key}&part={part}&playlistId={playlist_id}&maxResults={max_results}')

        # Return the data.
        return r.json()

    def get_yt_video_data(self, video_id: str):
        """
        Retrieve the YouTube snippet data from a given YouTube ID.
        :param video_id: the YouTube video's ID to retrieve the information of.
        :return: generic YouTube v3 API JSON response.
        """
        # Prepare the YouTube API v3 API key.
        key = self.app_db.credentials['api_youtube']

        # Preparing the request queries.
        part = 'snippet'

        # Fetching the data.
        with requests.Session() as s:
            r = s.get(
                self.YT_ENDPOINT_VIDEO_ITEMS + f'?key={key}&part={part}&id={video_id}')

        # Return the data.
        return r.json()

    def update_wp_homepage(
            self,
            autodetect_last_yt: bool = True,
            autodetect_last_ig: bool = True,
            custom_yt_link: str = '',
            custom_ig_img_path: str = ''
    ):
        """
        Updates the homepage of GKISalatiga.org according to the latest sunday service data.
        :param autodetect_last_yt: whether to autodetect the latest uploaded YouTube live-streaming.
        :param autodetect_last_ig: whether to automatically download service poster from Instagram.
        :param custom_yt_link: the custom YouTube stream link when "autodetect_last_yt" is False.
        :param custom_ig_img_path: the custom poster file path when "autodetect_last_ig" is False.
        :return: a success status (bool) and a log message (str).
        """
        try:

            # DEBUG! Please comment out after use.
            # print(autodetect_last_yt, autodetect_last_ig, custom_yt_link, custom_ig_img_path)

            # Preparing the poster image.
            msg = 'Preparing the service poster image ...'
            self.anim.set_prog_msg(10, msg)
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            if not autodetect_last_ig:
                # Finding the selected file's mime type. [2]
                file_mimetype = MimeTypes.guess_mimetype(custom_ig_img_path)

                if not file_mimetype.startswith('image/'):
                    raise InvalidMimeTypeException

                local_ig_poster_path = custom_ig_img_path

            else:
                # Obtaining the latest Instagram post using "instascrap".
                msg = 'Scraping the latest Instagram post ...'
                self.anim.set_prog_msg(15, msg)
                Lg('lib.uploader.Uploader.update_wp_homepage', msg)
                poster_img_path, poster_meta = self.get_latest_ig_post(self.IG_ACCOUNT_USERNAME)

                # Prepare the poster path.
                local_ig_poster_path = poster_img_path

            # Scraping the latest "Warta Jemaat" data.
            msg = 'Fetching the latest "Warta Jemaat" posts ...'
            self.anim.set_prog_msg(25, msg)
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            all_warta = self.get_latest_warta()

            # The latest warta link.
            latest_warta = all_warta[0]['link']

            # Scraping the latest "Tata Ibadah" data.
            msg = 'Fetching the latest "Tata Ibadah" posts ...'
            self.anim.set_prog_msg(40, msg)
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            all_liturgi = self.get_latest_liturgi()

            # The latest liturgi link.
            latest_liturgi = all_liturgi[0]['link']

            # Preparing the latest YouTube streaming URL.
            msg = 'Preparing the YouTube embedded streaming URL ...'
            self.anim.set_prog_msg(55, msg)
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            if not autodetect_last_yt:
                # Parsing the YouTube link's query parameters. [8]
                parsed_url = urlparse(custom_yt_link)
                v = parse_qs(parsed_url.query)['v'][0]
                target_yt_embed = self.YT_EMBED_PREFIX + f'/{v}'

                # DEBUG! Please comment out on production.
                # print(f'v:{v}')

            else:
                # Calling the YouTube API v3 to retrieve the latest "Kebaktian Umum" URL.
                msg = 'Fetching the latest "Kebaktian Umum" YouTube streaming videos ...'
                self.anim.set_prog_msg(60, msg)
                Lg('lib.uploader.Uploader.update_wp_homepage', msg)
                all_video_data = self.get_latest_yt_playlist(self.YT_PLAYLIST_KEBAKTIAN_UMUM)

                # Filtering only one latest video, then obtain its videoId.
                latest_video_id = all_video_data['items'][0]['snippet']['resourceId']['videoId']

                # Building the embedded YouTube video link.
                target_yt_embed = self.YT_EMBED_PREFIX + f'/{latest_video_id}'

            # Upload the PDF thumbnail to WordPress.
            msg = 'Uploading the Instagram poster to WordPress ...'
            self.anim.set_prog_msg(75, msg)
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            wp_media_upload_response = self.upload_wp_media(
                local_ig_poster_path, f'Sunday service featured poster image')
            poster_image_link = wp_media_upload_response['guid']['raw']

            # The "Ibadah GKI Salatiga" homepage post id.
            homepage_post_id = 52

            # DEBUG! Please comment out on production.
            # print(target_yt_embed, latest_liturgi, latest_warta, poster_image_link)

            # Creating the post.
            content = f'''
            <!-- AUTO-GENERATED BY "SIMON PETRUS", AN ADMINISTRATOR DASHBOARD APP OF GKI SALATIGA -->
            <!-- SEE MORE IN THIS GITHUB REPOSITORY: https://github.com/gkisalatiga/simon-petrus -->
            <p><iframe title="YouTube video player" src="{target_yt_embed}" width="560" height="315" frameborder="0" allowfullscreen="allowfullscreen"></iframe></p>
            <p><a id="link-liturgi" href="{latest_liturgi}"><img class="alignnone wp-image-4171" src="https://i0.wp.com/gkisalatiga.org/wp-content/uploads/2023/07/2-1.png?resize=218%2C66" alt="Tautan Liturgi" width="218" height="66" /></a></p>
            <p><a id="link-warta" href="{latest_warta}"><img class="alignnone wp-image-4170" src="https://i0.wp.com/gkisalatiga.org/wp-content/uploads/2023/07/WARTA-JEMAAT-1.png?resize=218%2C66" alt="Tautan Warta Jemaat" width="218" height="66" /></a></p>
            <figure class="wp-block-image size-large"><img src="{poster_image_link}" alt="Poster Kebaktian Umum" width="100%" /></figure>
            '''.strip()
            msg = 'Updating the WordPress homepage. This will not be very long ...'
            self.anim.set_prog_msg(90, msg)
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            j = self.edit_wp_post(homepage_post_id, content)

            # Did we make it? Has the homepage been updated?
            if j['id'] != homepage_post_id:
                raise MalformedHttpResponseJSON

            # Done! It's finished.
            self.anim.set_progress(100)
            return True, 'The GKISalatiga.org homepage has been successfully updated and refreshed!'

        except HttpError as e:
            msg = f'An unknown HTTP error has just occurred. Maybe check your internet connection?: {e}'
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            return False, msg

        except InvalidMimeTypeException as e:
            msg = f'You must select a valid image file!: {e}'
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            return False, msg

        except MalformedHttpResponseJSON as e:
            msg = f'The response JSON payload is malformed! Please check your credential or internet connection: {e}'
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            return False, msg

        except UploadFileSizeTooBig as e:
            msg = f'The selected file size must be less than or equal to 5 MiB: {e}'
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            return False, msg

        except Exception as e:
            msg = f'Unknown error is detected: {e}'
            Lg('lib.uploader.Uploader.update_wp_homepage', msg)
            traceback.print_exc()
            return False, msg


    def upload_google_drive(self, file_path: str, mime: str, folder_id: str, save_as: str):
        """
        Upload a file to Simon Petrus' specific Google Drive drop folder.
        :param file_path: the absolute file path of the file that will be uploaded.
        :param mime: the mimetype of the uploaded file.
        :param folder_id: the target Google Drive folder ID to which the file will be uploaded.
        :param save_as: the name of the file to save as in Google Drive.
        :return: generic Google Drive API JSON (dict) response.
        """
        # Using the following method, the maximum file size is 5 MiB.
        if os.path.getsize(file_path) >= 5000000:
            raise UploadFileSizeTooBig(
                'This method does not yet support uploading files larger than 5 MiB to Google Drive')

        # Parsing the token as the API credential.
        token_json_location = self.prefs.TEMP_DIRECTORY + os.sep + 'gdrive_token.json'

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if not os.path.exists(token_json_location):
            with open(token_json_location, 'w') as fo:
                json.dump(self.app_db.credentials.get('authorized_drive_oauth'), fo)
        creds = Credentials.from_authorized_user_file(token_json_location, self.GOOGLE_DRIVE_SCOPES)
        # If the credential has expired, refresh it.
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save the refreshed credentials for the next run
            with open(token_json_location, 'w') as token:
                token.write(creds.to_json())

        # Attempt to upload the requested file to Google Drive.
        # Error-catching is done at level of the method which called this function.
        service = build('drive', 'v3', credentials=creds)

        # This parent folder ID is a publicly shared Google Drive folder.
        parent_gdrive_folder = folder_id

        # Call the Drive v3 API to upload a file
        # SOURCE: https://developers.google.com/drive/api/guides/manage-uploads#multipart
        file_metadata = {'name': save_as, 'parents': [parent_gdrive_folder]}
        media = MediaFileUpload(file_path, mimetype=mime)
        # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields='*')
            .execute()
        )

        return file

    def upload_liturgi(self, pdf_path: str, post_title: str):
        """
        Upload Tata Ibadah to Google Drive, then post it to WordPress.
        :return: a boolean of upload status and an upload message string.
        :param pdf_path: the string pointing to the respective PDF file's path.
        :param post_title: the title of the WordPress post.
        """
        try:
            # Finding the selected file's mime type. [2]
            file_mimetype = MimeTypes.guess_mimetype(pdf_path)

            if file_mimetype != 'application/pdf':
                raise InvalidMimeTypeException

            # Generate the thumbnail.
            msg = 'Generating the PDF thumbnail ...'
            self.anim.set_prog_msg(10, msg)
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            thumbnail_path = self.generate_pdf_thumbnail(pdf_path)

            # Upload the PDF file to Google Drive.
            msg = 'Uploading PDF to Google Drive ...'
            self.anim.set_prog_msg(45, msg)
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            gdrive_response = self.upload_google_drive(pdf_path, file_mimetype, self.GDRIVE_ID_LITURGI, f'{post_title}.pdf')
            gdrive_pdf_id = gdrive_response['id']

            # Upload the PDF thumbnail to WordPress.
            msg = 'Uploading thumbnail to WordPress ...'
            self.anim.set_prog_msg(75, msg)
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            wp_media_upload_response = self.upload_wp_media(
                thumbnail_path, f'Featured image for the post "{post_title}"')
            featured_image_id = wp_media_upload_response['id']

            # Determining the post categories and tags.
            cats = [67]
            tags = [34, 68]

            # Creating the post.
            content = f'''
            <!-- AUTO-GENERATED BY "SIMON PETRUS", AN ADMINISTRATOR DASHBOARD APP OF GKI SALATIGA -->
            <!-- SEE MORE IN THIS GITHUB REPOSITORY: https://github.com/gkisalatiga/simon-petrus -->
            <iframe src="https://drive.google.com/file/d/{gdrive_pdf_id}/preview" width="640" height="480" allow="autoplay"></iframe>
            <p>
                <a href="https://drive.usercontent.google.com/u/0/uc?export=download&id={gdrive_pdf_id}">
                    <strong>{post_title}</strong>
                </a>
            </p>
            '''.strip()
            msg = 'Posting the post to WordPress ...'
            self.anim.set_prog_msg(90, msg)
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            self.upload_wp_post(post_title, content, featured_image_id, cats, tags)

            # Done! It's finished.
            self.anim.set_progress(100)
            return True, 'The "Tata Ibadah" post has been successfully uploaded and created!'

        except HttpError as e:
            msg = f'An unknown HTTP error has just occurred. Maybe check your internet connection?: {e}'
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            return False, msg

        except InvalidMimeTypeException as e:
            msg = f'You must select a valid PDF file ending in ".pdf" file extension!: {e}'
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            return False, msg

        except UploadFileSizeTooBig as e:
            msg = f'The selected PDF file size must be less than or equal to 5 MiB: {e}'
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            return False, msg

        except Exception as e:
            msg = f'Unknown error is detected: {e}'
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            traceback.print_exc()
            return False, msg

    def upload_warta(self, pdf_path: str, post_title: str):
        """
        Upload Warta Jemaat to Google Drive, then post it to WordPress.
        :return: a boolean of upload status and an upload message string.
        :param pdf_path: the string pointing to the respective PDF file's path.
        :param post_title: the title of the WordPress post.
        """
        try:
            # Finding the selected file's mime type. [2]
            file_mimetype = MimeTypes.guess_mimetype(pdf_path)

            if file_mimetype != 'application/pdf':
                raise InvalidMimeTypeException

            # Generate the thumbnail.
            msg = 'Generating the PDF thumbnail ...'
            self.anim.set_prog_msg(10, msg)
            Lg('lib.uploader.Uploader.upload_warta', msg)
            thumbnail_path = self.generate_pdf_thumbnail(pdf_path)

            # Upload the PDF file to Google Drive.
            msg = 'Uploading PDF to Google Drive ...'
            self.anim.set_prog_msg(45, msg)
            Lg('lib.uploader.Uploader.upload_warta', msg)
            gdrive_response = self.upload_google_drive(pdf_path, file_mimetype, self.GDRIVE_ID_WARTA_JEMAAT, f'{post_title}.pdf')
            gdrive_pdf_id = gdrive_response['id']

            # Upload the PDF thumbnail to WordPress.
            msg = 'Uploading featured image (thumbnail) to WordPress ...'
            self.anim.set_prog_msg(75, msg)
            Lg('lib.uploader.Uploader.upload_warta', msg)
            wp_media_upload_response = self.upload_wp_media(
                thumbnail_path, f'Featured image for the post "{post_title}"')
            featured_image_id = wp_media_upload_response['id']

            # Determining the post categories.
            cats = [4]
            tags = [34, 10]

            # Creating the post.
            content = f'''
            <!-- AUTO-GENERATED BY "SIMON PETRUS", AN ADMINISTRATOR DASHBOARD APP OF GKI SALATIGA -->
            <!-- SEE MORE IN THIS GITHUB REPOSITORY: https://github.com/gkisalatiga/simon-petrus -->
            <iframe src="https://drive.google.com/file/d/{gdrive_pdf_id}/preview" width="640" height="480" allow="autoplay"></iframe>
            <p>
                <a href="https://drive.usercontent.google.com/u/0/uc?export=download&id={gdrive_pdf_id}">
                    <strong>{post_title}</strong>
                </a>
            </p>
            '''.strip()
            msg = 'Posting the post to WordPress ...'
            self.anim.set_prog_msg(90, msg)
            Lg('lib.uploader.Uploader.upload_warta', msg)
            self.upload_wp_post(post_title, content, featured_image_id, cats, tags)

            # Done! It's finished.
            self.anim.set_progress(100)
            return True, 'The "Warta Jemaat" post has been successfully uploaded and created!'

        except HttpError as e:
            msg = f'An unknown HTTP error has just occurred. Maybe check your internet connection?: {e}'
            Lg('lib.uploader.Uploader.upload_warta', msg)
            return False, msg

        except InvalidMimeTypeException as e:
            msg = f'You must select a valid PDF file ending in ".pdf" file extension!: {e}'
            Lg('lib.uploader.Uploader.upload_warta', msg)
            return False, msg

        except UploadFileSizeTooBig as e:
            msg = f'The selected PDF file size must be less than or equal to 5 MiB: {e}'
            Lg('lib.uploader.Uploader.upload_warta', msg)
            return False, msg

        except Exception as e:
            msg = f'Unknown error is detected: {e}'
            Lg('lib.uploader.Uploader.upload_warta', msg)
            traceback.print_exc()
            return False, msg

    def upload_wp_media(self, file_path: str, file_caption: str):
        """
        Upload a media file to GKISalatiga.org.
        :param file_caption: the caption of the file to upload.
        :param file_path: the file to upload.
        :return: generic WordPress JSON response.
        """
        wp_token = self.app_db.credentials['wp_authorization']

        # Prepare the request header.
        header = {'Authorization': 'Basic ' + wp_token}

        # Begin the requests dispatching.
        with requests.Session() as s:
            # We need to first open this site, since the API blocks cross-origin requests.
            r = s.get(self.WP_DOMAIN_TARGET)

            # Preparing the media to upload.
            with open(file_path, 'rb') as fo:
                media = {
                    'file': fo,
                    'caption': file_caption
                }

                # Uploading the file.
                r = s.post(self.WP_ENDPOINT_MEDIA, headers=header, files=media)
                return r.json()

    def upload_wp_post(self, title: str, post_content: str, featured_image: int, cats: list, tags: list = []):
        """
        Upload a regular WordPress post to remote.
        :param tags: the tag to apply to the post.
        :param title: the title of the WP post.
        :param post_content: the HTML content of the WP post.
        :param featured_image: the featured image ID that will be displayed at the very top of the post.
        :param cats: the category IDs of this particular post, as an array.
        :return: generic WordPress API JSON response.
        """
        wp_token = self.app_db.credentials['wp_authorization']

        # Prepare the request header.
        header = {'Authorization': 'Basic ' + wp_token}

        # Begin the requests dispatching.
        with requests.Session() as s:
            # We need to first open this site, since the API blocks cross-origin requests.
            r = s.get(self.WP_DOMAIN_TARGET)

            # Preparing the post content to upload.
            post_data = {
                'title': title,
                'content': post_content,
                'categories': cats,
                'tags': tags,
                'featured_media': featured_image,
                'status': 'publish',
                'comment_status': 'closed'
            }

            # Uploading the new post as "published".
            r = s.post(self.WP_ENDPOINT_POSTS, headers=header, json=post_data)
            return r.json()
