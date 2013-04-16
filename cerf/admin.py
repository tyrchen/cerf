# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import logging
from django.contrib import admin
from cerf.forms import CaseForm, ExamForm, InterviewForm
from cerf.models import Case, Exam, Interview, Answer
from cerf.utils.helper import generate_authcode, get_url_by_conf

__author__ = 'tchen'
logger = logging.getLogger(__name__)

class TagAdminMixin(object):
    def tag(self, obj):
        return ', '.join([unicode(t) for t in obj.tags.all()])
    tag.short_description = 'Tags'


class CaseAdmin(admin.ModelAdmin, TagAdminMixin):
    form = CaseForm
    raw_id_fields = ('author', )
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
    raw_id_fields = ('case', )


class ExamAdmin(admin.ModelAdmin, TagAdminMixin):
    form = ExamForm
    raw_id_fields = ('author',)
    list_display = ('name', 'author', 'case', 'tag', 'created', 'modified')
    list_filter = (
        'author',
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
    raw_id_fields = ('candidate', 'manager', 'exam')
    list_display = ('candidate', 'manager', 'instruction', 'authcode', 'exam', 'scheduled', 'started', 'time_spent', 'created', 'modified')
    list_filter = (
        'manager',
    )

    def instruction(self, obj):
        return '<a href="%s" target="_blank">Print</a>' % get_url_by_conf('interview_instruction', [obj.id])
    instruction.short_description = 'Instruction'
    instruction.allow_tags = True

    def save_form(self, request, form, change):
        obj = super(InterviewAdmin, self).save_form(request, form, change)
        if not change:
            obj.manager = request.user
            obj.authcode = generate_authcode()
        return obj


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Case, CaseAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Answer, AnswerAdmin)