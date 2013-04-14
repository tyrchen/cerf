# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import logging
from django.contrib import admin
from cerf.forms import CaseForm, ExamForm, InterviewForm
from cerf.models import Case, Exam, Interview

__author__ = 'tchen'
logger = logging.getLogger(__name__)

class TagAdminMixin(object):
    def tag(self, obj):
        return ', '.join([unicode(t) for t in obj.tags.all()])
    tag.short_description = 'Tags'


class CaseAdmin(admin.ModelAdmin, TagAdminMixin):
    form = CaseForm
    list_display = ('name', 'type', 'level', 'category', 'author', 'tag', 'created', 'modified')
    list_filter = (
        ('level'), ('type'), ('category'), ('author')
    )

    search_fields = ['name',]


    def save_form(self, request, form, change):
        obj = super(CaseAdmin, self).save_form(request, form, change)
        if not change:
            obj.author = request.user
        return obj

class ExamCaseInlineAdmin(admin.TabularInline):
    model = Exam.cases.through

class ExamAdmin(admin.ModelAdmin, TagAdminMixin):
    form = ExamForm
    list_display = ('name', 'author', 'case', 'tag', 'created', 'modified')
    list_filter = (
        ('author'),
    )

    search_fields = ['name', ]
    inlines = [
        ExamCaseInlineAdmin,
    ]

    def case(self, obj):
        return '<br/>'.join(['case%s: %s' % (c.position, c.case) for c in obj.get_examcases()])
    case.short_description = 'Cases'
    case.allow_tags = True

    def save_form(self, request, form, change):
        obj = super(ExamAdmin, self).save_form(request, form, change)
        if not change:
            obj.author = request.user
        return obj

class InterviewAdmin(admin.ModelAdmin):
    form = InterviewForm
    list_display = ('candidate', 'manager', 'resume', 'exam', 'finished', 'created', 'modified')
    list_filter = (
        ('manager'),
    )

    def finished(self, obj):
        return obj.report == ''
    finished.short_description = 'Finished'

    def save_form(self, request, form, change):
        obj = super(InterviewAdmin, self).save_form(request, form, change)
        if not change:
            obj.manager = request.user
        return obj

admin.site.register(Case, CaseAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Interview, InterviewAdmin)