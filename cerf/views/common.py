# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from cerf.models import Interview
from cerf.utils.helper import get_url_by_conf, info_response

__author__ = 'tchen'
logger = logging.getLogger(__name__)


def redirect_user(user):
    if user.is_staff:
        return HttpResponseRedirect(get_url_by_conf('interviews'))

    try:
        latest_interview = Interview.objects.filter(candidate=user).order_by('-created')[0]
        return HttpResponseRedirect(get_url_by_conf('interview', [latest_interview.id]))
    except:
        return info_response('Cannot find your interview record, please contact your hiring manager.')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(get_url_by_conf('signin'))

        return redirect_user(user)


class SigninView(TemplateView):
    template_name = 'cerf/signin.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect_user(user)
            else:
                return info_response('Your account is inactive. Please contact your hiring manager.')
        else:
            return HttpResponseRedirect(get_url_by_conf('signin'))


class SignoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

