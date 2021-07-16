#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
from json import loads
from re import search
from datetime import datetime
from io import StringIO
from html.parser import HTMLParser

# third-party modules
from phonenumbers import parse, is_valid_number
from password_strength import PasswordPolicy
from base64 import b64decode


# own modules
from app.config import BaseConfig


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."



def get_logged_user(self, req):

    if 'X-Hoovada-Jwt' in req.headers:
        auth_token = req.headers['X-Hoovada-Jwt']
    else:
        return None

    user_id = decode_base64_jwt_payload(auth_token)
    if user_id is None:
        return None

    return user_id

    
def decode_base64_jwt_payload(auth_token):
    try:
        missing_padding = 4-len(data)%4 
        if missing_padding:
            auth_token += '=' * missing_padding 
        payload = loads(base64.b64decode(auth_token).decode())
        return payload['sub']
    except Exception as e:
        print(e.__str__())
        return None


def is_valid_phone_code(phone, code, user):
    try:
        service = BaseConfig.VERIFICATION_SID
        verification_check = client.verify.services(service).verification_checks.create(to=phone, code=code)
        if verification_check.status == "approved":
            current_time = datetime.utcnow()
            difference = current_time - user.verification_sms_time
            return difference.seconds <= BaseConfig.LIMIT_VERIFY_SMS_TIME
        return False
    
    except Exception as e:
        print(e.__str__())
        return False


def is_valid_phone_number(phone_number):

    try:
        phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(phone_number)
    except Exception as e:
        print(e.__str__())
        return False


def is_valid_password(password):
    try:
        policy = PasswordPolicy.from_names(length=8,)
        return True if len (policy.test(password)) == 0 else False
    except Exception as e:
        print(e.__str__())
        return False


def is_valid_email(email):

    try:
        regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return search(regex, email) is not None
    except Exception as e:
        print(e.__str__())
        return False


def is_valid_display_name(display_name):

    try:
        if len(display_name) > 20:
            return False

        if display_name.lower() in ['undefined', 'khách', 'ẩn danh', 'null']:
            return False

        return True
    except Exception as e:
        print(e.__str__())
        return False

def create_random_string(length):
    from string import ascii_letters, digits
    from random import choices
    random_string = ''.join(choices(ascii_letters + digits, k = length))
    return random_string


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

