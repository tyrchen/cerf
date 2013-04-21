# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from cerf.models import Exam

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class ExamListView(ListView):
    template_name = 'cerf/exams/exam_list.html'
    model = Exam
    paginate_by = 20
    context_object_name = 'exam_list'

    def get_context_data(self, **kwargs):
        context_data = super(ExamListView, self).get_context_data(**kwargs)
        context_data['page_type'] = 'exams'
        return context_data

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExamListView, self).dispatch(*args, **kwargs)


class ExamView(DetailView):
    model = Exam
    template_name = 'cerf/exams/exam.html'
