# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.utils.const import MATCH_PK
from cerf.views.exams import ExamListView, ExamView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url(r'^$', ExamListView.as_view(), name='exams'),
                       url(r'^%s/$' % MATCH_PK, ExamView.as_view(), name='exam'),
                       )
