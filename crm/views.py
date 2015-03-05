# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponseNotAllowed, Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist

from .utils import root_exists, access_permitted, get_title


class Content(View):
    """
    Base CRM view.
    """
    content_root = 'content'

    def get_content_root(self):
        return self.content_root

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
        content_root = self.get_content_root()
        if not root_exists(content_root):
            raise Http404
        if access_permitted(path, restrict, request):
            path = 'index' if path is None else path
            path = path[:-1] if path[-1] == '/' else path
            template_path = '/'.join([content_root, path + '.html'])
            try:
                return render(request, template_path, {'title': get_title(path)})
            except TemplateDoesNotExist as e:
                raise Http404(e)
        else:
            raise HttpResponseNotAllowed
content = Content.as_view()