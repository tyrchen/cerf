# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from cerf.models import Case

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class CaseListView(ListView):
    template_name = 'cerf/cases/case_list.html'
    model = Case
    paginate_by = 20
    context_object_name = 'case_list'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CaseListView, self).dispatch(*args, **kwargs)


class CaseView(DetailView):
    pass
