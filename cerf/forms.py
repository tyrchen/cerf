# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from cerf.models import Case, Exam, Interview, Answer


class CaseForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Case
        exclude = ('author', )


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ('author', )


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('author', )


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        exclude = ('candidate', 'manager', 'started', 'authcode', 'time_spent', 'report')
