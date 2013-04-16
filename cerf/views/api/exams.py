# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from cerf.models import Exam
from cerf.views.api.serializers import ExamCaseSerializer

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class ExamAPIView(RetrieveAPIView):
    model = Exam

    def get(self, request, *args, **kwargs):
        pk = self.args[0]
        try:
            exam = self.model.objects.get(pk=pk)
        except:
            return Response({})
        cases = []
        for case in exam.get_examcases():
            cases.append(ExamCaseSerializer(case).data)

        return Response({
            'name': exam.name,
            'description': exam.description,
            'cases': cases
        })