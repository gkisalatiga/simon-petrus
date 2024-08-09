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
    [6] Backtracing in Python
    - https://www.perplexity.ai/search/python-how-to-backtrace-error-RSgsVAVwRhuuQ2skpNfR_g
"""

from datetime import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from magic import Magic as Mgc
from pdf2image import convert_from_path
import json
import os
import requests
import traceback

from lib.database import AppDatabase
from lib.exceptions import InvalidMimeTypeException, UploadFileSizeTooBig
from lib.logger import Dumper as Dmp
from lib.logger import Logger as Lg
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

    # The WordPress domain target.
    WP_DOMAIN_TARGET = 'https://gkisalatiga.org'

    # The WordPress REST API endpoint for uploading media.
    WP_ENDPOINT_MEDIA = f'{WP_DOMAIN_TARGET}/wp-json/wp/v2/media'

    # The WordPress REST API endpoint for uploading pages.
    WP_ENDPOINT_PAGES = f'{WP_DOMAIN_TARGET}/wp-json/wp/v2/pages'

    # The WordPress REST API endpoint for uploading posts.
    WP_ENDPOINT_POSTS = f'{WP_DOMAIN_TARGET}/wp-json/wp/v2/posts'

    def __init__(
            self, anim_window: ScreenLoadingAnimation = None,
            global_pref: SavedPreferences = None,
            global_db: AppDatabase = None
    ):
        self.anim = anim_window
        self.prefs = global_pref
        self.app_db = global_db

    def generate_pdf_thumbnail(self, pdf_path: str):
        """
        Generate PDF overview thumbnail as an image.
        :param pdf_path: the string pointing to the respective PDF file's path.
        :return: the generated thumbnail's image path.
        """
        # Determining the output filename.
        filename_without_extension = os.path.splitext(os.path.split(pdf_path)[1])[0]
        output_file = self.prefs.TEMP_DIRECTORY + os.sep + filename_without_extension + '.png'

        # Extract the first page of the PDF file as an image. [3]
        images = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=1)

        # Save the thumbnail.
        images[0].save(output_file, 'JPEG')
        Lg('lib.uploader.Uploader.generate_pdf_thumbnail', f'PDF thumbnail has been saved to: {output_file}')

        return output_file

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
            file_mimetype = Mgc(mime=True).from_file(pdf_path)

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

        except Exception as e:
            msg = f'Unknown error is detected: {e}'
            Lg('lib.uploader.Uploader.upload_liturgi', msg)
            traceback.print_exc()
            return False, msg

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

    def upload_warta(self, pdf_path: str, post_title: str):
        """
        Upload Warta Jemaat to Google Drive, then post it to WordPress.
        :return: a boolean of upload status and an upload message string.
        :param pdf_path: the string pointing to the respective PDF file's path.
        :param post_title: the title of the WordPress post.
        """
        try:
            # Finding the selected file's mime type. [2]
            file_mimetype = Mgc(mime=True).from_file(pdf_path)

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

        except Exception as e:
            msg = f'Unknown error is detected: {e}'
            Lg('lib.uploader.Uploader.upload_warta', msg)
            traceback.print_exc()
            return False, msg

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
