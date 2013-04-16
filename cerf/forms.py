# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from cerf.models import Case, Exam, Interview


class CaseForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Case
        exclude = ('author', )


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ('author', )


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        exclude = ('manager', 'started', 'authcode', 'time_spent')
