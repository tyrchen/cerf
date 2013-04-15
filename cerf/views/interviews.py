# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.views.generic import ListView
from cerf.models import Interview

__author__ = 'tchen'
logger = logging.getLogger(__name__)

class InterviewListView(ListView):
    template_name = 'cerf/interviews/interview_list.html'
    model = Interview
    paginate_by = 20
    context_object_name = 'interview_list'
