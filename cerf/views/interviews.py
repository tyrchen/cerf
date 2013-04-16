# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.db.models import Avg
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


class InterviewCreateView(CreateView):
    form_class = InterviewForm
    template_name = 'cerf/interviews/interview_create.html'


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
            interview.report = interview.generate_report()
        context_data['report'] = json.loads(interview.report)

        exam = interview.exam
        candidate_count = exam.interview_set.count()
        avg_time_spent = Interview.objects.filter(exam=exam).aggregate(Avg('time_spent'))
        context_data['avg_time_spent'] = int(avg_time_spent['time_spent__avg'])
        context_data['candidate_count'] = candidate_count

        return context_data