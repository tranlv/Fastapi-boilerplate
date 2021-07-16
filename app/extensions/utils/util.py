#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
import hashlib
from json import loads
from re import search
from base64 import b64decode
from datetime import datetime, timedelta
from io import StringIO
from html.parser import HTMLParser

# third-party modules
from jwt import encode
import phonenumbers
from flask import render_template
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from password_strength import PasswordPolicy
from twilio.rest import Client

# own modules
from app.config import BaseConfig
from app.extensions.db import db
from app.extensions.mail import mail


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


client = Client(username=BaseConfig.TWILIO_ACCOUNT_SID, password=BaseConfig.TWILIO_AUTH_TOKEN)

def encode_file_name(filename):
    now = datetime.now()
    encoded = hashlib.sha224(filename.encode('utf8')).hexdigest()
    return '{}{}'.format(now.isoformat(), encoded)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=BaseConfig.SECURITY_SALT)


def send_email(to, subject, template, sender=(BaseConfig.MAIL_USERNAME, BaseConfig.MAIL_DEFAULT_SENDER)):
    if to:
        msg = Message(subject, sender=sender, recipients=[to], html=template, charset='utf-8')
        mail.send(msg)


def send_confirmation_email(to, user=None):    
    token = generate_confirmation_token(email=to)
    confirm_url = '{}/?page=signup_success&token={}&email={}'.format(BaseConfig.DOMAIN_URL, token, to)
    html = render_template('confirmation.html', confirm_url=confirm_url, user=user)
    send_email(to, 'Hoovada- Xác thực tài khoản!', html, sender=(BaseConfig.AUTHENTICATION_MAIL_USERNAME,BaseConfig.AUTHENTICATION_MAIL_SENDER))


def send_password_reset_email(to):    
    token = generate_confirmation_token(email=to)
    html = render_template('reset_password.html', token=token)
    send_email(to, 'Hoovada - Thay đổi mật khẩu!', html, sender=(BaseConfig.AUTHENTICATION_MAIL_USERNAME, BaseConfig.AUTHENTICATION_MAIL_SENDER))


def get_response_message(message):    
    html = render_template('response.html', message=message)
    return html


def encode_auth_token(user, delta=timedelta(days=30, seconds=5)):    
    try:
        payload = {
            'exp': datetime.utcnow() + delta,
            'iat': datetime.utcnow(),
            'iss': "admin@hoovada.com",
            'sub': str(user.id)
        }

        return encode(
            payload,
            BaseConfig.PRIVATE_KEY,
            algorithm='RS256'
        )

    except Exception as e:
        print(e.__str__())
        return None


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


def send_verification_sms(to='', user=None):
    try: 
        service = BaseConfig.VERIFICATION_SID
        verification = client.verify.services(service).verifications.create(to=to, channel='sms')

        if verification and verification.sid and user:
            user.verification_sms_time = datetime.utcnow()
            db.session.commit()
        
        return verification.sid
    except Exception as e:
        print(e.__str__())
        db.session.rollback()
        raise e


def confirm_token(token, expirations=300):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email_or_phone = serializer.loads(token, salt=BaseConfig.SECURITY_SALT, max_age=expirations)
        return email_or_phone
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


def get_logged_user(self, req):

    if 'X-Hoovada-Jwt' in req.headers:
        auth_token = req.headers['X-Hoovada-Jwt']
    else:
        return None

    user_id = decode_base64_jwt_payload(auth_token)
    if user_id is None:
        return None

    try:
        user = db.get_model('User').query.filter_by(id=int(user_id)).first()
        return user
    except Exception as e:
        print(e.__str__())
        return None


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

