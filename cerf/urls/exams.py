# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.views.exams import ExamListView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url('^$', ExamListView.as_view(), name='exams'),
                       )
