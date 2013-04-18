# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.utils.const import MATCH_TEXT
from cerf.views.api.answers import AnswerAPIView, AnswerListCreateAPIView
from cerf.views.api.exams import ExamAPIView
from cerf.views.api.interviews import InterviewAPIView

__author__ = 'tchen'

urlpatterns = patterns('',
    url('^interviews/%s/$' % MATCH_TEXT, InterviewAPIView.as_view(), name='interview_api'),
    url('^exams/%s/$' % MATCH_TEXT, ExamAPIView.as_view(), name='exam_api'),
    url('^answers/$', AnswerListCreateAPIView.as_view(), name='answer_list_api'),
    url('^answers/%s/$' % MATCH_TEXT, AnswerAPIView.as_view(), name='answer_api'),

    )