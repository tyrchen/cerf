# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View, TemplateView
from cerf.models import Interview
from cerf.utils.helper import get_url_by_conf

__author__ = 'tchen'
logger = logging.getLogger(__name__)

class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(get_url_by_conf('signin'))

        if user.is_staff:
            return HttpResponseRedirect(get_url_by_conf('interviews'))

        try:
            latest_interview = Interview.objects.filter(candidate=user).order_by('-created')[0]
            return HttpResponseRedirect(get_url_by_conf('interview', [latest_interview.id]))
        except:
            return HttpResponse('Cannot find your interview record, please contact your hiring manager.')

class SigninView(TemplateView):
    template_name = 'cerf/signin.html'

    def post(self, request, *args, **kwargs):
        pass


