"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] Get day of the week name from date
    - https://www.perplexity.ai/search/how-to-use-the-kf5-widget-in-p-vJOvyW0yRnmFHwYQmBoB2g
    [2] Split http query parameters
    - https://www.perplexity.ai/search/python-urllib-how-to-separate-zUZmLT2.T_qsUTmxy8hXvw
"""

from datetime import datetime as dt
from urllib.parse import urlparse, parse_qs


class StringValidator(object):

    # The Indonesian locale of day of the week.
    LOCALE_DAY_OF_WEEK = [
        'Senin',
        'Selasa',
        'Rabu',
        'Kamis',
        'Jumat',
        'Sabtu',
        'Minggu'
    ]

    # The Indonesian locale for the name of the months.
    LOCALE_MONTH_NAME = [
        'Januari',
        'Februari',
        'Maret',
        'April',
        'Mei',
        'Juni',
        'Juli',
        'Agustus',
        'September',
        'Oktober',
        'November',
        'Desember'
    ]

    def __init__(self):
        pass

    @staticmethod
    def get_date():
        """
        Gets date in YYYY-MM-DD format.
        :return: date string in YYYY-MM-DD format.
        """
        now = dt.now()
        y = now.year
        m = now.month
        d = now.day
        return f'{y}-{StringValidator.zero_pad(m, 2)}-{StringValidator.zero_pad(d, 2)}'

    @staticmethod
    def get_day_of_week(year: int, month: int, day: int):
        """
        Returns date (consisting of year, month, and day) into the Indonesian
        locale for days of the week.
        :return: integer, where 0 is Monday, 1 is Tuesday, and so on.
        """
        # We are living in the 2nd millennium.
        if year < 100:
            year = 2000 + year

        # Find the weekday.
        new_date = dt(year, month, day, 0, 0, 0)
        return new_date.weekday()

    @staticmethod
    def get_full_date(preformatted_date: str):
        """
        Converts "YYYY-MM-DD" date string to Indonesian date locale similar to "Senin, 23 Agustus 2024".
        :param preformatted_date: the preformatted date string in YYYY-MM-DD pattern.
        :return: date in Indonesian locale similar to "Senin, 23 Agustus 2024"
        """
        b = preformatted_date.split('-')
        c = StringValidator.LOCALE_DAY_OF_WEEK[StringValidator.get_day_of_week(int(b[0]), int(b[1]), int(b[2]))]
        d = StringValidator.LOCALE_MONTH_NAME[int(b[1]) - 1]
        return f'{c}, {b[2]} {d} {b[0]}'

    @staticmethod
    def get_gdrive_full_url(gdrive_id: str):
        """ Return the proper, shareable Google Drive link from a GDrive ID. """
        return 'https://drive.google.com/drive/folders/' + gdrive_id

    @staticmethod
    def get_youtube_id_from_link(yt_url: str):
        """
        Obtains the YouTube ID from a given link. [2]
        :param yt_url: the YouTube video link.
        :return: YouTube video id.
        """
        parsed_url = urlparse(yt_url)
        v = parse_qs(parsed_url.query)['v'][0]
        return v

    @staticmethod
    def get_youtube_link_from_id(yt_id: str):
        """
        Obtains a valid YouTube link from a given YT video id.
        :param yt_id: the YouTube ID which will be converted to link.
        :return: a YouTube video URL.
        """
        return f'https://www.youtube.com/watch?v={yt_id}'

    @staticmethod
    def get_youtube_playlist_id_from_link(yt_url: str):
        """
        Self-explanatory.
        """
        return parse_qs(urlparse(yt_url).query)['list'][0]

    @staticmethod
    def get_youtube_playlist_link_from_id(playlist_id: str):
        """
        Obtains a valid YouTube playlist link from a given playlist ID.
        :param playlist_id: the playlist ID.
        :return: a YouTube playlist URL.
        """
        return f'https://www.youtube.com/playlist?list={playlist_id}'

    @staticmethod
    def zero_pad(num: int, digits: int):
        """
        Zero-pad any integer with leading zeros.
        :param num: the number to pad with zero.
        :param digits: the returned string's number of digits/characters (must be strictly greater than or equal to "num")
        :return: a zero-padded string.
        """
        if len(str(num)) > digits:
            return str(num)
        else:
            return ('0' * (digits - len(str(num)))) + str(num)
