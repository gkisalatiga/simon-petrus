"""
Resolve resource path when packaged using PyInstaller.
SOURCE: https://stackoverflow.com/q/31836104
Answers by Rainer Niemann (https://stackoverflow.com/users/5570586/rainer-niemann)
and Nautilius (https://stackoverflow.com/users/5168024/nautilius)
licensed under CC BY-SA to the respective authors.
"""

import os
import sys
from lib.logger import Logger as Lg


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception as e:
        Lg('lib.external.meipass.resource_path', f'Error encountered: {e}')
        base_path = os.path.dirname(sys.argv[0])

    full_path = os.path.join(base_path, relative_path)
    Lg('lib.external.meipass.resource_path', f'Full resource path generated: {full_path}')
    return full_path
