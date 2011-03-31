# -*- coding: utf-8 -*-
from django_ipgeobase.models import IPGeoBase


class IpGeoBaseMiddleware(object):
    def process_request(self, request):
        request.ip = request.META['REMOTE_ADDR']
        request.ip = '109.87.208.224'
        request.ip_location = None
        addr = IPGeoBase.objects.by_ip(request.ip)
        if not addr:
            return
        request.ip_location = addr[0]
