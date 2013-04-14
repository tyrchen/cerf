# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import logging
from django.utils.text import slugify
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from cerf.utils import const
from taggit.managers import TaggableManager

__author__ = 'tchen'
logger = logging.getLogger(__name__)

class Case(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_case'
        verbose_name = 'Case'
        ordering = ['level']

    name = models.CharField('Unique Name', max_length=48, help_text='Please provide a unique name for the case to be easily memorized')
    description = models.CharField('Description', max_length=1024, help_text='The detailed description of case - you can write it in Markdown')
    type = models.IntegerField('Type', choices=const.CASE_TYPE_CHOICES, default=const.CASE_TYPE_CODING)
    level = models.IntegerField('Level', choices=const.CASE_LEVEL_CHOICES, default=const.CASE_LEVEL_COMPETENT)
    category = models.IntegerField('Category', choices=const.CASE_CATEGORY_CHOICES, default=const.CASE_CATEGORY_GENERAL)
    solution = models.TextField('Suggested Solution', default='', blank=True)
    author = models.ForeignKey(User)
    language = models.IntegerField('Language', choices=const.CASE_LANG_CHOICES, default=const.CASE_LANG_C)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    tags = TaggableManager()

    @property
    def slug(self):
        return slugify(self.name)

    def __unicode__(self):
        return self.name

class Anwser(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_answer'
        verbose_name = 'Answer'
        ordering = ['-created']

    case = models.ForeignKey('Case')
    author = models.ForeignKey(User)
    interview = models.ForeignKey('Interview')
    content = models.TextField('Content', default='', blank=True)
    created = CreationDateTimeField()

    def __unicode__(self):
        return '%s: %s' % (self.author.username, self.case)

    def url(self):
        return '/media/interview/%s/%s.tgz' % (self.interview_id, self.case.slug)


