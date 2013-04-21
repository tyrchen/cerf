# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
import markdown
from cerf.models import Interview, Exam, Case
from cerf.utils.helper import get_url_by_conf, info_response, get_average

__author__ = 'tchen'
logger = logging.getLogger(__name__)


def redirect_user(user):
    return HttpResponseRedirect('/')


class IndexView(TemplateView):
    template_name = 'cerf/index.html'
    max_items = 5

    def get_items(self, qset):
        items = []
        for item in qset.order_by('-created')[:self.max_items]:
            month, day = item.created.strftime('%b %d').split(' ')
            items.append({
                'title': item.get_name(),
                'description': item.get_description(),
                'url': item.get_absolute_url(),
                'day': day,
                'month': month
            })
        return items

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        interview_qs = Interview.objects.all()
        exam_qs = Exam.objects.all()
        case_qs = Case.objects.all()
        context['stat'] = {
            'interviews': interview_qs.count(),
            'exams': exam_qs.count(),
            'cases': case_qs.count(),
            'avg_exam_time': get_average(Interview.objects.all(), 'time_spent')
        }

        context['interviews'] = self.get_items(interview_qs)
        context['exams'] = self.get_items(exam_qs)
        context['cases'] = self.get_items(case_qs)

        context['page_type'] = 'home'

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


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

    def get_context_data(self, **kwargs):
        context = super(StaticFileView, self).get_context_data(**kwargs)
        from django.conf import settings
        import os
        filename = os.path.join(settings.PROJECT_ROOT, self.filename)
        title, content = codecs.open(filename, encoding='utf8').read().split('====')

        content = markdown.markdown(content)
        context['flatpage'] = {
            'title': title,
            'content': content,
        }

        return context
