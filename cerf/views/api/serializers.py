# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers
from cerf.models import Interview, Case, Exam, ExamCase
from cerf.models.cases import Answer
from cerf.utils import const
from cerf.utils.helper import get_choice_string, get_lang_extentions


__author__ = 'tchen'
logger = logging.getLogger(__name__)


class UserField(serializers.RelatedField):
    def to_native(self, value):
        return value.get_full_name()


class LangField(serializers.CharField):
    def to_native(self, value):
        return get_choice_string(value, const.CASE_LANG_CHOICES)


class LangExtentionField(serializers.CharField):
    def to_native(self, value):
        return ', '.join(get_lang_extentions(value, const.CASE_LANG_EXTENTIONS))


class InterviewSerializer(serializers.ModelSerializer):
    candidate = UserField(read_only=True)
    candidate_id = serializers.IntegerField(source='candidate.id', read_only=True)
    manager = UserField(read_only=True)
    exam = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Interview
        exclude = ('resume',)


class CaseSerializer(serializers.ModelSerializer):
    lang = LangField(source='language', read_only=True)

    class Meta:
        model = Case
        fields = ('name', 'description', 'code', 'lang')


class ExamCaseSerializer(serializers.ModelSerializer):
    cid = serializers.IntegerField(source='case.id')
    name = serializers.CharField(source='case.name')
    description = serializers.CharField(source='case.description')
    code = serializers.CharField(source='case.code')
    lang = LangField(source='case.language', read_only=True)
    extentions = LangExtentionField(source='case.language', read_only=True)

    class Meta:
        model = ExamCase
        fields = ('cid', 'name', 'description', 'code', 'lang', 'extentions', 'position')


# this seems doesn't work, so workaround in view
class ExamSerializer(serializers.ModelSerializer):
    cases = ExamCaseSerializer(many=True)

    class Meta:
        model = Exam
        fields = ('name', 'description', 'cases')


class AnswerSerializer(serializers.ModelSerializer):
    interview = serializers.PrimaryKeyRelatedField()
    case = serializers.PrimaryKeyRelatedField()
    author = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Answer
        fields = ('interview', 'case', 'author', 'content')