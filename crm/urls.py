# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url, include


def get_urls(**kwargs):
    """
    Generates a URLCONF based on the setting CRM_VIEW for routing requests to the CRM framework. CRM_VIEW can be
    anything can be accepted in the view position of `url()`.
    """
    return include([url(r'^$', settings.CRM_VIEW, kwargs=kwargs, name='content'),
                    url(r'^(.*)/$', settings.CRM_VIEW, kwargs=kwargs, name='content')])