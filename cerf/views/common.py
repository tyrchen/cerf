# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import logging
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View, TemplateView
import markdown
from cerf.utils.helper import get_url_by_conf, info_response

__author__ = 'tchen'
logger = logging.getLogger(__name__)


def redirect_user(user):
    return HttpResponseRedirect(get_url_by_conf('interviews'))


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


class StaticFileView(TemplateView):
    filename = ''
    template_name = 'flatpages/default.html'

    def get(self, request, *args, **kwargs):
        from django.conf import settings
        import os
        filename = os.path.join(settings.PROJECT_ROOT, self.filename)
        title, content = codecs.open(filename, encoding='utf8').read().split('====')

        content = markdown.markdown(content)
        variables = RequestContext(request, {
            'flatpage': {'title': title, 'content': content}
        })
        return render_to_response(self.template_name, variables)
