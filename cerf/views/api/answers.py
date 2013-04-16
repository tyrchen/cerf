# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import generics
from cerf.models.cases import Answer
from cerf.views.api.serializers import AnswerSerializer


__author__ = 'tchen'
logger = logging.getLogger(__name__)


class AnswerAPIView(generics.ListCreateAPIView):
    model = Answer
    serializer_class = AnswerSerializer

    def get_queryset(self):
        id = self.request.GET.get('id', '')
        if id:
            return Answer.objects.filter(interview_id=id)
        return Answer.objects.all()

