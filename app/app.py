#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from logging.config import dictConfig

# third-party modules
from flask import Flask, g, request, session
from flask_cors import CORS
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from sqlalchemy_utils import create_database, database_exists

# own modules
from app import config_by_name
from app.extensions.models import *
from app.extensions.utils.util import get_logged_user
from app.extensions.mail import mail
from app.extensions.db import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# Config logging output
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def init_basic_app():

    Flask.get_logged_user = get_logged_user
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_by_name[app.config['ENV']])

    @app.before_request
    def before_request():
        g.current_user = app.get_logged_user(request)
        
        if 'role' not in session:
            session['role'] = 'user'

        g.current_user_is_admin = g.current_user.admin if g.current_user is not None else False
        g.endorsed_topic_id = None
        g.friend_belong_to_user_id = None
        g.mutual_friend_ids = []
        
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

# Prometheus metrics exporter
#metrics = GunicornInternalPrometheusMetrics(init_basic_app())
#metrics.register_default(
#    metrics.counter(
#        'by_path_counter', 'Request count by request paths',
#        labels={'path': lambda: request.path}
#    )
#)

def init_app():
    app = init_basic_app()

    CORS(app)

    url = app.config['SQLALCHEMY_DATABASE_URI']

    if not database_exists(url):
        create_database(url, app.config['DB_CHARSET'])

    db.init_app(app)

    mail.init_app(app)

    return app
