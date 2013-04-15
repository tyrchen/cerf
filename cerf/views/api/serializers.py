# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import serializers
from cerf.models import Interview


__author__ = 'tchen'
logger = logging.getLogger(__name__)


class UserField(serializers.RelatedField):
    def to_native(self, value):
        return value.get_full_name()


class ExamField(serializers.RelatedField):
    def to_native(self, value):
        return value.id


class InterviewSerializer(serializers.ModelSerializer):
    candidate = UserField(read_only=True)
    manager = UserField(read_only=True)
    exam = ExamField(read_only=True)

    class Meta:
        model = Interview
        exclude = ('authcode',)
