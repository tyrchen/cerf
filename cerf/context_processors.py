# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

__author__ = 'tchen'
logger = logging.getLogger(__name__)

from django.contrib.sites.models import Site


def site(request):
    return {
        'site': Site.objects.get_current()
    }
