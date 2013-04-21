# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cerf.utils.const import MATCH_PK
from cerf.views.cases import CaseListView, CaseView

__author__ = 'tchen'

urlpatterns = patterns('',
                       url(r'^$', CaseListView.as_view(), name='cases'),
                       url(r'^%s/$' % MATCH_PK, CaseView.as_view(), name='case'),
                       )
