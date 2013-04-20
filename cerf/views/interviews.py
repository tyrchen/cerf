# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from cerf.forms import InterviewForm
from cerf.models import Interview

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class InterviewListView(ListView):
    template_name = 'cerf/interviews/interview_list.html'
    model = Interview
    paginate_by = 20
    context_object_name = 'interview_list'

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
        avg_time_spent = Interview.objects.filter(exam=exam).aggregate(Avg('time_spent'))
        try:
            context_data['avg_time_spent'] = int(avg_time_spent['time_spent__avg'])
        except:
            context_data['avg_time_spent'] = 0
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
