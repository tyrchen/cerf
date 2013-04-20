# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.contrib import admin
from cerf.forms import CaseForm, ExamForm, InterviewForm
from cerf.models import Case, Exam, Interview, Answer, Applicant
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
    list_display = ('id', 'name', 'type', 'level', 'category', 'author', 'tag', 'created', 'modified')
    list_filter = (
        ('level', ), ('type', ), ('category', ), ('author', )
    )

    search_fields = ['name', ]

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
    raw_id_fields = ('author', )
    list_display = ('name', 'author', 'case', 'tag', 'created', 'modified')
    list_filter = (
        ('author', ),
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
    raw_id_fields = ('applicant', 'manager', 'exam')
    list_display = ('id', 'applicant', 'manager', 'instruction', 'authcode', 'exam', 'scheduled', 'started', 'time_spent', 'created', 'modified')
    list_filter = (
        'manager',
    )

    actions = ['generate_report', 'reset']

    def instruction(self, obj):
        return '<a href="%s" target="_blank">Print</a>' % get_url_by_conf('interview_instruction', [obj.id])
    instruction.short_description = 'Instruction'
    instruction.allow_tags = True

    def generate_report(self, request, queryset):
        for interview in queryset:
            interview.generate_report()
    generate_report.short_description = 'Re-generate interview report'

    def reset(self, request, queryset):
        for interview in queryset:
            interview.reset()
    reset.short_description = "Reset interview"

    def save_form(self, request, form, change):
        obj = super(InterviewAdmin, self).save_form(request, form, change)
        if not change:
            obj.manager = request.user
            obj.authcode = generate_authcode()
        return obj


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'interview', 'applicant', 'code')

    def code(self, obj):
        return '<pre>%s</pre>' % obj.content
    code.short_description = 'Code'
    code.allow_tags = True


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'resume', 'created')


admin.site.register(Case, CaseAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Applicant, ApplicantAdmin)
