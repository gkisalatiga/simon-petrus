"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""
from datetime import datetime as dt

# This parameter determines whether logging and dumping are allowed.
# They're useful especially in production.
IS_DUMPING_ALLOWED = True
IS_LOGGING_ALLOWED = True


class Dumper(object):
    def __init__(self, dump_tag: str, dump_string: str):
        if IS_DUMPING_ALLOWED:
            now = dt.now()
            print(f'::: [{now}] [{dump_tag}] ==================== STRING DUMP ====================')
            print(dump_string)

            # The following may not be necessary.
            # print('.' * 25)


class Logger(object):
    def __init__(self, log_tag: str, log_string: str):
        if IS_LOGGING_ALLOWED:
            now = dt.now()
            print(f'::: [{now}] [{log_tag}] + {log_string}')
