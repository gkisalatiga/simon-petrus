"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)

---
REFERENCES:
    [1] Get day of the week name from date
    - https://www.perplexity.ai/search/how-to-use-the-kf5-widget-in-p-vJOvyW0yRnmFHwYQmBoB2g
"""

from datetime import datetime as dt


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

    def get_day_of_week(self, year: int, month: int, day: int):
        """
        Returns date (consisting of year, month, and day) into the Indonesian
        locale for days of the week.
        :return: integer, where 0 is Monday, 1 is Tuesday, and so on.
        """
        # We are living in the 2nd millennium.
        year = 2000 + year

        # Find the weekday.
        new_date = dt(year, month, day, 0, 0, 0)
        return new_date.weekday()
