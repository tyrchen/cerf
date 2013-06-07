# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
import json
import time
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from cerf.models import Interview

__author__ = 'tchen'
logger = logging.getLogger(__name__)

'''
{
    "success": 1,
    "result": [
        {
            "id: 293,
            "title": "Event 1",
            "url": "http://someurl.com",
            "class": 'event-important',
            start: 12039485678,
            end: 1234576967
        },
        ...
    ]
}
'''


class EventListAPIView(View):
    model = Interview

    def get_queryset(self):

        today = datetime.today()
        weekstart = datetime(today.year, today.month, today.day - today.weekday())
        return self.model.objects.filter(scheduled__gte=weekstart)

    def get(self, request, *args, **kwargs):
        results = self.get_queryset()

        count = len(results)
        data = {}
        if count > 0:
            data['success'] = 1
            data['result'] = [{'id': i.id,
                               'title': i.get_reserve_info(),
                               'url': i.get_absolute_url(),
                               'class': 'event-info',
                               'start': int(time.mktime(i.scheduled.timetuple())) * 1000,
                               'end': int(time.mktime((i.scheduled + timedelta(hours=1)).timetuple())) * 1000
                               } for i in results]
        else:
            data['success'] = 1
            data['result'] = []

        return HttpResponse(json.dumps(data))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(EventListAPIView, self).dispatch(request, *args, **kwargs)
