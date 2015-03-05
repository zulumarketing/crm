# -*- coding: utf-8 -*-

from django.conf.urls import url, include


def get_urls(**kwargs):
    return include([url(r'^$', 'crm.views.content', kwargs=kwargs, name='content'),
                    url(r'^(.*)/$', 'crm.views.content', kwargs=kwargs, name='content')])