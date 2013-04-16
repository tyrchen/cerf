# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import logging
from django.utils.text import slugify
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from taggit.managers import TaggableManager
from cerf.models import Answer
from cerf.utils import const
from cerf.utils.helper import get_choice_string

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class Exam(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_exam'
        verbose_name = 'Exam'
        ordering = ['-created']

    name = models.CharField('Exam Name', unique=True, max_length=64, help_text='Please provide a unique exam name, like MTS4 platform exam')
    description = models.TextField('Exam Description', default='', blank=True)
    author = models.ForeignKey(User)
    cases = models.ManyToManyField('Case', through='ExamCase', verbose_name='Cases')
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    tags = TaggableManager()

    @property
    def slug(self):
        return slugify(self.name)

    def __unicode__(self):
        return self.name

    def get_cases(self):
        return self.cases.order_by('examcase_set')

    def get_examcases(self):
        return ExamCase.objects.filter(exam=self)

class ExamCase(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_exam_case'
        verbose_name = 'Exam Case'
        ordering = ['position']
        unique_together = (('exam', 'case'))
    case = models.ForeignKey('Case', related_name='examcase_set')
    exam = models.ForeignKey('Exam')
    position = models.IntegerField('Position')

    def __unicode__(self):
        return self.case


class Interview(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_interview'
        verbose_name = 'Interview'
        ordering = ['-created']

    candidate = models.ForeignKey(User, related_name='interview_candidates')
    manager = models.ForeignKey(User, related_name='interview_managers')
    resume = models.FileField(upload_to='uploads/resumes')
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
        self.time_spent = (datetime.now() - self.started).seconds / 60
        self.generate_report(False)
        self.save()
        self.send_notification()

    def generate_report(self, save=True):
        from django.template import Template, Context
        from django.template.loader import get_template
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
            data['code'] = answer.content
            results.append(data)

        results = sorted(results, key=lambda item: item['position'])
        data = {
            'candidate': self.candidate.get_full_name(),
            'manager': self.manager.get_full_name(),
            'started': self.started,
            'time_spent': '%s minutes' % self.time_spent,
            'candidate_count_temp': '{{candidate_count_temp}}',
            'avg_time_spent_temp': '{{avg_time_spent_temp}}',
            'results': results
        }
        template = get_template('cerf/reports/%s' % settings.REPORT_TEMPLATE)
        self.report = template.render(Context(data))
        if save:
            self.save()

    def send_notification(self):
        pass

    def reset(self):
        self.started = self.time_spent = None
        self.report = ''
        Answer.objects.filter(interview=self).delete()
        self.save()