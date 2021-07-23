#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from functools import wraps

# third-party modules
from flask import g

# own modules

from app.extensions.utils.response import send_error
from . import messages


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.current_user
        if user is None:
            return send_error(message=messages.ERR_NOT_LOGIN, code=401)
        if user.is_deactivated:
            return send_error(message=messages.ERR_USER_DEACTIVATED, code=401)
        return f(*args, **kwargs)

    return decorated
