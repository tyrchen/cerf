# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from cerf.models import Interview
from cerf.views.api.serializers import InterviewSerializer

__author__ = 'tchen'
logger = logging.getLogger(__name__)


def get_valid_interview(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except:
        return None
    authcode = request.DATA.get('authcode', '')
    if interview.authcode == authcode:
        return interview
    return None


class InterviewAPIView(RetrieveUpdateAPIView):
    serializer_class = InterviewSerializer
    actions = ['start', 'finish', 'reset']

    def get_object(self, queryset=None):
        pk = self.args[0]
        return get_valid_interview(self.request, pk)

    def get(self, request, *args, **kwargs):
        interview = self.get_object()
        if not interview:
            return Response({})

        serializer = self.get_serializer(interview)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        action_name = request.DATA.get('action', '')
        if action_name not in self.actions:
            return Response({})

        interview = self.get_object()
        if not interview:
            return Response({})

        getattr(interview, action_name)()

        serializer = self.get_serializer(interview)
        return Response(serializer.data)
