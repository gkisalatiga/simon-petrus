"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""
from lib.preferences import SavedPreferences

class SetupOAUTH(object):

    def get_oauth_credential(self):
        # Parsing the token as the API credential.
        token_json_location = SavedPreferences.TEMP_DIRECTORY + os.sep + 'gdrive_token.json'

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if not os.path.exists(token_json_location):
            with open(token_json_location, 'w') as fo:
                json.dump(self.credentials.get('authorized_drive_oauth'), fo)
        creds = Credentials.from_authorized_user_file(token_json_location, self.GOOGLE_DRIVE_SCOPES)
        # If the credential has expired, refresh it.
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save the refreshed credentials for the next run
            with open(token_json_location, 'w') as token:
                token.write(creds.to_json())

    def write_oauth_refresh_token(self):
        """
        Write the Google OAUTH2.0 refresh token file to a volatile private temporary directory.
        :return: nothing.
        """
        