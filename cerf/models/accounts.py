# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import logging

__author__ = 'tchen'
logger = logging.getLogger(__name__)

class Account(AbstractBaseUser):
    candidate = models.BooleanField(default=False)

    def is_candidate(self):
        return self.candidate

