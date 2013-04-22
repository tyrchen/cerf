# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import logging
from django.utils.text import slugify
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from cerf.utils import const
from taggit.managers import TaggableManager
from cerf.utils.helper import get_choice_string

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
    code = models.TextField('Code', blank=True, default='', help_text='Leave this blank if you do not have initial code to let applicant work with')
    language = models.IntegerField('Language', choices=const.CASE_LANG_CHOICES, default=const.CASE_LANG_C)
    expected_time = models.IntegerField('Expected Time (in minutes)', default=20)
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
        return ('case', [self.id])

    def get_extentions(self):
        return const.CASE_LANG_EXTENTIONS[self.language]

    def get_name(self):
        return unicode(self)

    def get_description(self):
        return self.description

    def get_answer_stat(self):
        qs = Answer.objects.filter(case=self)
        return {
            'count': qs.count(),
        }

    def get_intro(self):
        stat = self.get_answer_stat()
        return '''This case is for __%s__ on __%s__.
                The category is __%s__.
                Coding language should be __%s__.
                Expected time spent on it is __%s minutes__.
                Total __%s__ exams use this case.''' % (
            get_choice_string(self.level, const.CASE_LEVEL_CHOICES),
            get_choice_string(self.type, const.CASE_TYPE_CHOICES),
            get_choice_string(self.category, const.CASE_CATEGORY_CHOICES),
            get_choice_string(self.language, const.CASE_LANG_CHOICES),
            self.expected_time,
            stat['count'],
        )

    def get_data(self):
        stat = self.get_answer_stat()
        return {
            'name': self.get_name(),
            'description': self.get_description(),
            'intro': self.get_intro(),
            'level': get_choice_string(self.level, const.CASE_LEVEL_CHOICES),
            'type': get_choice_string(self.type, const.CASE_TYPE_CHOICES),
            'category': get_choice_string(self.category, const.CASE_CATEGORY_CHOICES),
            'language': get_choice_string(self.language, const.CASE_LANG_CHOICES),
            'expected_time': self.expected_time,
            'solution': '<pre class="prettyprint linenums">%s</pre>' % self.solution if self.solution else '',
            'total_answers': stat['count'],
        }


class Answer(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_answer'
        verbose_name = 'Answer'
        ordering = ['interview', '-created']

    case = models.ForeignKey('Case')
    author = models.ForeignKey(User, null=True, blank=True)
    applicant = models.ForeignKey('Applicant')
    interview = models.ForeignKey('Interview')
    content = models.TextField('Content', default='', blank=True)
    created = CreationDateTimeField()

    def __unicode__(self):
        return '%s: %s' % (self.author.username, self.case)
