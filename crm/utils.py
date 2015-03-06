# -*- coding: utf-8 -*-

import re

from .exceptions import NotAllowed, LoginRequired


def check_permissions(path, restrictions, request) -> bool:
    """
    Enforces the rules specified in `CRM_CONTENT_RESTRICTIONS`.
    """
    for rule in restrictions:
        if rule['path'] == '*' or (path is not None and re.match(r'^' + rule['path'] + r'.+$', path)):
            pass
        else:
            continue
        if rule.get('in_group', None) and rule['in_group'] not in request.user.groups.values_list('name', flat=True):
            raise NotAllowed()
        if rule.get('login', False) and not request.user.is_authenticated():
            raise LoginRequired()


def get_title(path) -> str:
    """
    Parses a filename and returns a formatted title.
    """
    name = path.split('/')[-1]
    name = re.sub('--', ': ', name)
    name = re.sub('-', ' ', name)
    return name.title()


def get_slug(path) -> str:
    """"""
    path = 'index' if path is None else path
    path = path[:-1] if path[-1] == '/' else path
    return path