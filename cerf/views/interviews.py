# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from cerf.forms import InterviewForm
from cerf.models import Interview
from cerf.utils.helper import get_average

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class InterviewListView(ListView):
    template_name = 'cerf/interviews/interview_list.html'
    model = Interview
    paginate_by = 20
    context_object_name = 'interview_list'

    def get_context_data(self, **kwargs):
        context_data = super(InterviewListView, self).get_context_data(**kwargs)
        context_data['page_type'] = 'interviews'
        return context_data

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InterviewListView, self).dispatch(*args, **kwargs)


class InterviewCreateView(CreateView):
    form_class = InterviewForm
    template_name = 'cerf/interviews/interview_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InterviewCreateView, self).dispatch(*args, **kwargs)


class InterviewView(DetailView):
    template_name = 'cerf/interviews/interview.html'
    context_object_name = 'interview'
    model = Interview

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.args[0])

    def get_context_data(self, **kwargs):
        context_data = super(InterviewView, self).get_context_data(**kwargs)
        interview = context_data['interview']
        if not interview.report:
            interview.generate_report()
        context_data['report'] = json.loads(interview.report)

        exam = interview.exam
        applicant_count = exam.interview_set.count()
        context_data['avg_time_spent'] = get_average(Interview.objects.filter(exam=exam), 'time_spent')
        context_data['applicant_count'] = applicant_count

        return context_data

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InterviewView, self).dispatch(*args, **kwargs)


class InterviewInstructionView(DetailView):
    template_name = 'cerf/interviews/interview_instruction.html'
    context_object_name = 'interview'
    model = Interview

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.args[0])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InterviewInstructionView, self).dispatch(*args, **kwargs)
