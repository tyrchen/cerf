# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import logging
from django.utils.text import slugify
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from taggit.managers import TaggableManager
from cerf.utils.helper import get_average

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

    @models.permalink
    def get_absolute_url(self):
        return ('exam', [self.id])

    def get_cases(self):
        return self.cases.order_by('examcase_set')

    def get_examcases(self):
        return ExamCase.objects.filter(exam=self)

    def get_case_data(self):
        items = []
        for item in self.get_examcases():
            case = item.case.get_data()
            case['position'] = item.position
            items.append(case)

        return items

    def get_name(self):
        return unicode(self)

    def get_description(self):
        return self.description

    def get_interview_stat(self):
        from cerf.models import Interview
        qs = Interview.objects.filter(exam=self, time_spent__gt=10)
        return {
            'count': qs.count(),
            'avg_time_spent': get_average(qs, 'time_spent')
        }

    def get_intro(self):
        stat = self.get_interview_stat()
        return '''Total __%s__ applicants took this exam,
                  average time spent is __%s__ minutes.''' % (
            stat['count'], stat['avg_time_spent']
        )


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
