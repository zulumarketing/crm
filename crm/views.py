# -*- coding: utf-8 -*-

import os
import re

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponseNotAllowed, Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist


class Content(View):
    """

    """
    @staticmethod
    def _permitted(path, restrict, request) -> bool:
        return True

    @staticmethod
    def _root_exists(content_root) -> bool:
        if content_root is None:
            return False
        else:
            return os.path.exists(os.path.join(settings.BASE_DIR, 'crm/templates/', content_root))

    @staticmethod
    def _get_title(path):
        name = path.split('/')[-1]
        name = re.sub('--', ':', name)
        name = re.sub('-', ' ', name)
        return name.title()

    def get(self, request, path=None, restrict: [dict]=None):
        """
        :param request: Django request object.
        :param path: The incoming request path.
        :param restrict: Rules that limit access to content.
                         Available matching parameters are:
                            'sub_path': A sub-path of `content_root` or '*', which matches all pages.
                         Available access parameters are:
                            'to_group': Any group name.
                            'login': Required if True
        :return: Requested content if found, else 404.
        """
        content_root = request.brand['content_root']
        if not self._root_exists(content_root):
            raise Http404
        if self._permitted(path, restrict, request):
            path = 'index' if path is None else path
            path = path[:-1] if path[-1] == '/' else path
            template_path = '/'.join([content_root, path + '.html'])
            try:
                return render(request, template_path, {'title': self._get_title(path)})
            except TemplateDoesNotExist as e:
                raise Http404(e)
        else:
            raise HttpResponseNotAllowed
content = Content.as_view()