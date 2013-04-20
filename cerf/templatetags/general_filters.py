# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django import template
from django.template.defaultfilters import stringfilter

__author__ = 'tchen'
logger = logging.getLogger(__name__)
from markdown import markdown as md

register = template.Library()


@register.filter
@stringfilter
def trim(value):
    return value.strip()


@register.filter
@stringfilter
def markdown(value):
    return md(value)
