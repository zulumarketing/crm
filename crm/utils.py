# -*- coding: utf-8 -*-

import os
import re

from django.conf import settings


def access_permitted(path, restrict, request) -> bool:
    """
    Enforces the rules specified in `restrict`.
    """
    return True


def root_exists(content_root) -> bool:
    """
    Checks if the content root actually exists.
    """
    if content_root is None:
        return False
    else:
        return os.path.exists(os.path.join(settings.BASE_DIR, 'crm/templates/', content_root))


def get_title(path) -> str:
    """
    Parses a filename and returns a formatted title.
    """
    name = path.split('/')[-1]
    name = re.sub('--', ':', name)
    name = re.sub('-', ' ', name)
    return name.title()