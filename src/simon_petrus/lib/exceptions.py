"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] Get day of the week name from date
    - https://www.perplexity.ai/search/how-to-use-the-kf5-widget-in-p-vJOvyW0yRnmFHwYQmBoB2g
    [2] Creating custom exception in Python
    - https://www.perplexity.ai/search/creating-custom-exception-in-p-0BCmBy.vR9iBehKBWV3zHg
"""


class InvalidMimeTypeException(Exception):
    """ Errors related to undesired mimetype of a selected file. """
    def __repr__(self):
        return '<InvalidMimeTypeException: The file mimetype is unexpected or the file is corrupt>'

    __str__ = __repr__


class MalformedHttpResponseJSON(Exception):
    """ Errors related to invalid JSON format. """
    def __repr__(self):
        return '<MalformedHttpResponseJSON: The retrieved JSON file cannot be parsed by the back-end>'

    __str__ = __repr__


class MalformedSettingsJSON(Exception):
    """ Errors related to invalid app's settings' JSON structure, usually due to updates. """
    def __repr__(self):
        return '<MalformedSettingsJSON: The app\'s settings JSON file does not conform to the latest standard>'

    __str__ = __repr__


class UploadFileSizeTooBig(Exception):
    """ Upload file size limitation error (server API-side). """
    def __repr__(self):
        return '<UploadFileSizeTooBig: The API method cannot handle a file this big>'

    __str__ = __repr__
