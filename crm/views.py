# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.views.generic import View
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import redirect_to_login

from .utils import root_exists, check_permissions, get_title
from .exceptions import NotAllowed, LoginRequired

log = logging.getLogger('django.request')


class Content(View):
    """
    Base CRM view.
    """
    content_root = 'content'
    restrictions = tuple()

    def get_content_root(self):
        return self.content_root

    def get_restrictions(self) -> list:
        """
        Rules that limit access to content. Defined by the optional setting `CRM_CONTENT_RESTRICTIONS`.

        Available matching parameters are:

        'path': A sub-path of `content_root` or '*', which matches all pages. Sub-paths cover all child files
                    and directories.

        Available access parameters are:

        'to_group': Any group name.
        'login': Required if True.

        Restrictions are defined as a list of dicts specifying rules for access. Rules are evaluated until one denies
        access or the list ends.
        """
        try:
            return settings.CRM_CONTENT_RESTRICTIONS
        except AttributeError:
            return self.restrictions

    def get(self, request, path=None):
        """
        :param request: Django request object.
        :param path: The incoming request path.
        :return: Requested content if found, else 404.
        """
        content_root = self.get_content_root()
        restrictions = self.get_restrictions()
        if not root_exists(content_root):
            raise Http404
        try:
            check_permissions(path, restrictions, request)
        except NotAllowed:
            return HttpResponseForbidden('You are not allowed to access this resource!')
        except LoginRequired:
            return redirect_to_login(request.path)
        else:
            path = 'index' if path is None else path
            path = path[:-1] if path[-1] == '/' else path
            template_path = '/'.join([content_root, path + '.html'])
            try:
                return render(request, template_path, {'title': get_title(path)})
            except TemplateDoesNotExist as e:
                raise Http404(e)
        finally:
            log.exception('An unexpected error occurred!')
content = Content.as_view()