#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ

# third-party modules
from flask import url_for
from flask_restx import Api, Namespace, Resource

# own modules
from app.modules import *
from app.extensions.utils.response import send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class HTTPSApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        return url_for(self.endpoint('specs'), _external=True, _scheme=environ.get('WEB_PROTOCOL', 'https'))


ns_health = Namespace(name='healthz')
@ns_health.route('/')
class HealthCheck(Resource):
    def get(self):
        """ Use for Readiness and Liveness Probes"""
        return send_result()


def init_api():
    api = HTTPSApi(title='Hoovada APIs',
                   swagger='2.0',
                   version='1.0',
                   description='The Hoovada APIs',
                   authorizations={
                       'apikey': {
                           'type': 'apiKey',
                           'in': 'header',
                           'name': 'X-API-KEY'
                       }
                   },
                   security='apikey',
                   prefix='/api/v1',
                   doc=False)

    api.add_namespace(ns_health)
    api.add_namespace(ns_auth, '/auth')
    return api
