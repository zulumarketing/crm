# -*- coding: utf-8 -*-

import logging
import os
import re

from django.conf import settings
from django.views.generic import View
from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .utils import check_permissions, get_title, get_slug
from .exceptions import NotAllowed, LoginRequired

log = logging.getLogger('django.request')


class Content(View):
    """
    Base CRM view.
    """
    content_root = 'content'
    restrictions = tuple()

    def get_content_root(self):
        """Override this to provide dynamic content roots"""
        return self.content_root

    def get_restrictions(self) -> list:
        """
        Rules that limit access to content. Defined by the optional setting `CRM_CONTENT_RESTRICTIONS`.

        Available matching parameters are:

        'path': A sub-path of `content_root` or '*', which matches all pages. Sub-paths cover all child files
                    and directories.

        Available access parameters are:

        'in_group': Any group name.
        'login': Required if True.

        Restrictions are defined as a list of dicts specifying rules for access. Rules are evaluated until one denies
        access or the list ends.

        Rules are enforced by `crm.utils.check_permissions()`.
        """
        try:
            return settings.CRM_CONTENT_RESTRICTIONS
        except AttributeError:
            return self.restrictions

    def _nav_menu(self, current_prefix) -> {str: tuple}:
        """
        Generates a complete navigation tree for the current content root and a sub-tree for the current prefix.
        """
        add_prefix = lambda prefix, node: "{prefix}{node}".format(prefix=prefix + '/' if prefix != '' else prefix,
                                                                  node=node)
        search_path = os.path.join(settings.BASE_DIR, 'templates/crm/' + self.get_content_root())
        current_prefix = '/'.join(current_prefix.split('/')[:-1])
        current_path = os.path.join(search_path, current_prefix)

        def _generate_menu(base_path, prefix=''):
            """"""
            for node in os.listdir(base_path):
                node_slug = re.sub('.html', '', node)
                path = os.path.join(base_path, prefix, node)
                if os.path.isdir(path):
                    item = {'name': node,
                            'isdir': True,
                            'title': get_title(node_slug),
                            'children': None,
                            'slug': None}
                    children = os.listdir(path)
                    if children:
                        item['children'] = tuple(_generate_menu(path, prefix=item['name']))
                    if os.path.exists(os.path.join(path, 'index.html')):
                        item['slug'] = add_prefix(prefix, node_slug)
                    yield item
                else:
                    if prefix != '' and node_slug == 'index':
                        continue
                    yield {'name': add_prefix(prefix, node),
                           'isdir': False,
                           'title': get_title(node_slug),
                           'children': None,
                           'slug': add_prefix(prefix, node_slug)}
        return {'all': tuple(_generate_menu(search_path)),
                'current': tuple(_generate_menu(current_path, prefix=current_prefix))}

    def get(self, request, path=None):
        """
        :param request: Django request object.
        :param path: The incoming request path.
        :return: Requested content if found, else 404.
        """
        content_root = self.get_content_root()
        restrictions = self.get_restrictions()
        try:
            check_permissions(path, restrictions, request)
        except NotAllowed:
            raise PermissionDenied
        except LoginRequired:
            return redirect_to_login(request.path)
        else:
            path = get_slug(path)
            template_path = '/'.join(['crm', content_root, path + '.html'])
            try:
                return render(request, template_path, {'title': get_title(path), 'nav_menu': self._nav_menu(path)})
            except TemplateDoesNotExist as e:
                raise Http404(e)
content = Content.as_view()