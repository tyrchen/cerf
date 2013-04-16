# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.views.interviews import InterviewListView

__author__ = 'tchen'

urlpatterns = patterns('',
    url('^$', InterviewListView.as_view(), name='interviews'),
    url('^%s/$', InterviewView.as_view(), name="interview"),
)