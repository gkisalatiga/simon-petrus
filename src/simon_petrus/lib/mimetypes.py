"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

import filetype

class MimeTypes(object):

    @staticmethod
    def guess_mimetype(path: str):
        """
        Guess a given file's mimetype, even without file extension present.
        :param path: the path to the file which mimetype to guess
        :return: string of mimetype if mimetype detected, None if otherwise.
        """
        kind = filetype.guess(path)
        return None if kind is None else kind.mime
