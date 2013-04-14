# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.views.cases import CaseListView

__author__ = 'tchen'

urlpatterns = patterns('',
    url('^$', CaseListView.as_view(), name='cases'),
)