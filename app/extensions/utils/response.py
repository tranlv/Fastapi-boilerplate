#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def send_result(data=None, message='OK', code=200, status=True):

    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code


def send_error(data=None, message='Failed', code=400, status=False):

    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code


def paginated_result(query=None, message='OK', code=200, status=True):

    res = {
        'status': status,
        'code': code,
        'message': message,
        'page': query.page,
        'page_count': query.pages,
        'total': query.total,
        'data': query.items,
    }
    return res, code


def send_paginated_result(data=None, page=None, total=None, message='OK', code=200, status=True):

    res = {
        'status': status,
        'code': code,
        'message': message,
        'page': page,
        'total': total,
        'data': data,
    }

    return res, code


