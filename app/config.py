#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ

# third party modules

# own modules

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseConfig:

    # debug mode is turned off by default
    DEBUG = False
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    WEB_PROTOCOL = environ.get('WEB_PROTOCOL', 'https')
    DOMAIN_URL = WEB_PROTOCOL + '://' + environ.get('DOMAIN_ENDPOINT', 'localhost:5000')
    JSON_AS_ASCII = False

    # Authentication
    SECRET_KEY = environ.get('SECRET_KEY', 'abcd')
    SECURITY_SALT = environ.get('SECURITY_SALT', 'abcd')
    PRIVATE_KEY = environ.get('PRIVATE_KEY', '')

    # Email configuration
    MAIL_SERVER = environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = False

    MAIL_USERNAME =  environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD', '')

    # need to set this so that email can be sent
    MAIL_SUPPRESS_SEND = False
    TESTING = False

    AUTHENTICATION_MAIL_USERNAME = environ.get('AUTHENTICATION_MAIL_USERNAME', MAIL_USERNAME)
    AUTHENTICATION_MAIL_SENDER =  environ.get('AUTHENTICATION_MAIL_SENDER', MAIL_DEFAULT_SENDER)

    # mysql configuration
    DB_USER = environ.get('DB_USER', 'h00v3d3_db_us6r')
    DB_PASSWORD = environ.get('DB_PASSWORD', 'keUecZ4G47QE0vFBucxHTEW1DKwy4ZcI')
    DB_HOST = environ.get('DB_HOST', '139.59.252.127')
    DB_PORT = environ.get('DB_PORT', '3306')
    DB_NAME = environ.get('DB_NAME', 'hoovada')
    DB_CHARSET = 'utf8mb4'
    MAXIMUM_RETRY_ON_DEADLOCK = int(environ.get('MAXIMUM_RETRY_ON_DEADLOCK', 10))
    BCRYPT_LOG_ROUNDS = 13 # Number of times a password is hashed
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # social
    FACEBOOK_SECRET = environ.get('FACEBOOK_SECRET', '') 
    GRAPH_API_URL = 'https://graph.facebook.com/me?'
    FACEBOOK_FIELDS = [
        'id',
        'name',
        'address',
        'birthday',
        'email',
        'first_name',
        'gender',
        'last_name',
        'middle_name',
        'photos',
        'picture'
    ]
    GOOGLE_PROFILE_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
    
    # Twilio API credentials
    # (find here https://www.twilio.com/console)
    TWILIO_ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID', 'AC3bc87a9ca0dc5bcc55c263b00bd583c1')
    TWILIO_AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN', 'b2e699d59ef37fb757260178cdf1e3bb') # TEST Credentials
    # (create one here https://www.twilio.com/console/verify/services)
    VERIFICATION_SID = environ.get('VERIFICATION_SID', 'VAc2d0ecc3630b615db53742c8ef825fbd')
    LIMIT_VERIFY_SMS_TIME = 60 # 60seconds
    

class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    # if you want to use mysql 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
         user=BaseConfig.DB_USER,
         password=BaseConfig.DB_PASSWORD,
         host=BaseConfig.DB_HOST,
         port=BaseConfig.DB_PORT,
         name=BaseConfig.DB_NAME,
         charset=BaseConfig.DB_CHARSET
     )

class ProductionConfig(BaseConfig):
    """production configuration."""

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
         user=BaseConfig.DB_USER,
         password=BaseConfig.DB_PASSWORD,
         host=BaseConfig.DB_HOST,
         port=BaseConfig.DB_PORT,
         name=BaseConfig.DB_NAME,
         charset=BaseConfig.DB_CHARSET
     )
