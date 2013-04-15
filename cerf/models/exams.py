# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import logging
from django.utils.text import slugify
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from taggit.managers import TaggableManager

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
        unique_together = (('exam', 'case'), ('exam', 'position'))
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
    started = models.DateField('Started', null=True, blank=True)
    finished = models.DateTimeField('Finished', null=True, blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def start(self):
        if not self.started:
            self.started = datetime.now()
            self.save()
            return True
        return False

    def finish(self):
        if not self.started or self.finished:
            return False
        self.finished = datetime.now()
        self.save()


    def reset(self):
        self.started = self.finished = None
        self.save()