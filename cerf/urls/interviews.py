# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.utils import const
from cerf.views.interviews import InterviewListView, InterviewView, InterviewCreateView, InterviewInstructionView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url(r'^$', InterviewListView.as_view(), name='interviews'),
                       url(r'^create/$', InterviewCreateView.as_view(), name='interview_create'),

                       url(r'^%s/$' % const.MATCH_TEXT, InterviewView.as_view(), name="interview"),
                       url(r'^%s/instruction/$' % const.MATCH_TEXT, InterviewInstructionView.as_view(), name='interview_instruction'),

                       )
