# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.utils import const
from cerf.views.interviews import InterviewListView, InterviewView, InterviewCreateView

__author__ = 'tchen'

urlpatterns = patterns('',
    url('^$', InterviewListView.as_view(), name='interviews'),
    url('^create/$', InterviewCreateView.as_view(), name='interview_create'),

    url('^%s/$' % const.MATCH_TEXT, InterviewView.as_view(), name="interview"),

)