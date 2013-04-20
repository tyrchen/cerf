# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import logging
from django_extensions.db.fields import CreationDateTimeField

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class Applicant(models.Model):
    class Meta:
        app_label = 'cerf'
        db_table = 'cerf_applicant'
        verbose_name = 'Applicant'
        ordering = ['-created']

    name = models.CharField('Name', max_length=16)
    resume = models.FileField(upload_to='uploads/resumes', null=True, blank=True)
    created = CreationDateTimeField()

    def __unicode__(self):
        return self.name

    # just to keep the same with existing interface
    def get_full_name(self):
        return self.name
