# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.utils.const import MATCH_TEXT
from cerf.views.api.interviews import InterviewAPIView

__author__ = 'tchen'

urlpatterns = patterns('',
    url('^interviews/%s/$' % MATCH_TEXT, InterviewAPIView.as_view(), name='interview_api'),
)