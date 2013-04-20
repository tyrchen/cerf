# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import json
from django.contrib.auth.models import User
from django.db import models
import logging
from django.utils.html import escape
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from cerf.models import Answer, ExamCase
from cerf.utils import const
from cerf.utils.helper import get_choice_string

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class Interview(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_interview'
        verbose_name = 'Interview'
        ordering = ['-created']

    # this field is obsolete, should be phased out later
    candidate = models.ForeignKey(User, related_name='interview_candidate_obsoletes', null=True, blank=True)
    # the new candidate
    applicant = models.ForeignKey('Applicant')
    manager = models.ForeignKey(User, related_name='interview_managers')

    exam = models.ForeignKey('Exam')
    report = models.TextField('Report', default='', blank=True, help_text='Do not edit this, since it is generated automatically')

    authcode = models.CharField('Auth Code', max_length=32, help_text='Do not edit this, since it is generated automatically')

    scheduled = models.DateTimeField('Scheduled')
    started = models.DateTimeField('Started', null=True, blank=True)
    time_spent = models.IntegerField('Time spent(minutes)', null=True, blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def start(self):
        if not self.started:
            self.started = datetime.now()
            self.save()
            return True
        return False

    def finish(self):
        if not self.started or self.time_spent:
            return False
        self.time_spent = (datetime.now() - self.started).seconds / 60 + 1  # make minimum 1 minutes
        self.generate_report(False)
        self.save()
        self.send_notification()

    def generate_report(self, save=True):
        answers = Answer.objects.filter(interview=self).select_related()
        results = []
        for answer in answers:
            case = answer.case
            data = dict()
            data['position'] = ExamCase.objects.get(exam=self.exam_id, case=case).position
            data['name'] = case.name
            data['description'] = case.description
            data['level'] = get_choice_string(case.level, const.CASE_LEVEL_CHOICES)
            data['type'] = get_choice_string(case.type, const.CASE_TYPE_CHOICES)
            data['category'] = get_choice_string(case.category, const.CASE_CATEGORY_CHOICES)
            data['language'] = get_choice_string(case.language, const.CASE_LANG_CHOICES)
            data['expected_time'] = case.expected_time
            data['code'] = '<pre class="prettyprint linenums">%s</pre>' % escape(answer.content)
            results.append(data)

        results = sorted(results, key=lambda item: item['position'])
        data = {
            'name': self.exam.name,
            'description': self.exam.description,
            'applicant': self.applicant.get_full_name(),
            'manager': self.manager.get_full_name(),
            'started': self.started.isoformat() if self.started else '',
            'time_spent': self.time_spent if self.time_spent else 0,
            'results': results
        }
        #template = get_template('cerf/reports/%s' % settings.REPORT_TEMPLATE)
        #self.report = template.render(Context(data))
        self.report = json.dumps(data)
        if save:
            self.save()

    def send_notification(self):
        pass

    def reset(self):
        self.started = None
        self.time_spent = None
        self.report = ''
        Answer.objects.filter(interview=self).delete()
        self.save()
