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
    def __init__(self, message):
        super().__init__(message)


class MalformedHttpResponseJSON(Exception):
    def __init__(self, message):
        super().__init__(message)


class UploadFileSizeTooBig(Exception):
    def __init__(self, message):
        super().__init__(message)
