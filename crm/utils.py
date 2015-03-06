# -*- coding: utf-8 -*-

import os
import re

from django.conf import settings

from .exceptions import NotAllowed, LoginRequired


def check_permissions(path, restrictions, request) -> bool:
    """
    Enforces the rules specified in `CRM_CONTENT_RESTRICTIONS`.
    """
    for rule in restrictions:
        if rule['path'] == '*' or re.match(r'^' + rule['path'] + r'.+$', path):
            pass
        else:
            continue
        if rule.get('in_group', None) and rule['in_group'] not in request.user.groups.values_list('name', flat=True):
            raise NotAllowed()
        if rule.get('login', False) and not request.user.is_authenticated():
            raise LoginRequired()


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