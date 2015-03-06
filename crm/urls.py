# -*- coding: utf-8 -*-
"""
Generates a URLCONF based on the setting CRM_VIEW for routing requests to the CRM framework. CRM_VIEW can be
anything can be accepted in the view position of `url()`.
"""

from django.conf import settings
from django.conf.urls import url, patterns

try:
    crm_view = settings.CRM_VIEW
except AttributeError:
    crm_view = 'crm.views.content'


urlpatterns = patterns('', url(r'^$', crm_view, name='content'), url(r'^(.*)/$', crm_view, name='content'))