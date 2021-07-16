#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.extensions.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AuthDto(Dto):
    api = Namespace('auth')

    model_sms_register = api.model('sms_register', {
        'display_name': fields.String(required=False, description='User display name'),
        'phone_number': fields.String(required=True, description='The phone number used for registration'),
        'password': fields.String(required=True, description='The password - at least 8 characters, 1 number, 1 special symbol'),
        'password_confirm': fields.String(required=True, description='The confirm password'),
        'is_policy_accepted': fields.Boolean(required=True, default=False, description='The policy acceptance status'),
    })
    
    model_confirm_sms = api.model('confirm_sms', {
        'phone_number': fields.String(required=True, description='The phone number used for registration'),
        'code': fields.String(required=True, description='The sms code sent for confirmation')
    })
    
    model_resend_confirmation_sms = api.model('resend_confirmation_sms', {
        'phone_number': fields.String(required=True, description='The phone_number used for registration'),
    })
    
    model_sms_login_with_password = api.model('sms_login_with_password', {
        'phone_number': fields.String(required=True, description='The phone number used for registration'),
        'password': fields.String(required=True, description='The password - at least 8 characters, 1 number, 1 special symbol'),
    })
    
    model_sms_login_with_code = api.model('sms_login_with_code', {
        'phone_number': fields.String(required=True, description='The phone number used for login'),
    })
    
    model_sms_login_with_code_confirm = api.model('sms_login_with_code_confirm', {
        'phone_number': fields.String(required=True, description='The phone number that used for login'),
        'code': fields.String(required=True, description='The sms code for login'),
    })

    model_email_pasword_registration = api.model('register', {
        'display_name': fields.String(required=False, description='The name to display after login'),
        'email': fields.String(required=True, description='The user email used for registration'),
        'password': fields.String(required=True, description='The password - at least 8 characters, 1 number, 1 special symbol'),
        'password_confirm': fields.String(required=True, description='The confirm password'),
        'is_policy_accepted': fields.Boolean(required=True, default=False, description='The policy acceptance status'),
    })

    model_email_pasword_registration_confirm = api.model('reset_password_email', {
        'token': fields.String(required=True, description='The token sent to email for registration'),
    })

    model_login = api.model('login', {
        'email': fields.String(required=True, description='The user email used for registration'),
        'password': fields.String(requried=True, description='The password - at least 8 characters, 1 number, 1 special symbol')
    })

    model_social_login = api.model('social_login', {
        'access_token': fields.String(required=True, description='The token get from login FB or Google'),
    })

    model_password_reset_email = api.model('reset_password_email', {
        'email': fields.String(required=True, description='The email used for reset password request with email'),
    })

    model_password_reset_email_confirm = api.model('reset_password_email', {
        'token': fields.String(required=True, description='The token sent to email for password reset confirmation'),
    })

    model_reset_password_phone = api.model('reset_password_phone', {
        'phone_number': fields.String(required=True, description='The phone number for reset password request'),
    })

    model_reset_password_phone_confirm = api.model('reset_password_phone_confirm', {
        'phone_number': fields.String(required=True, description='The phone number for reset password request'),
        'code': fields.String(required=True, description='The OTP code sent through SMS'),
    })

    model_change_password_token = api.model('change_password_token', {
        'reset_token': fields.String(required=True, description='The token for confirmation'),
        'token_type': fields.String(required=True, choices=('email', 'phone'), description='The type of token to confirm (\'email\'/\'phone\')'),
        'password': fields.String(required=True, description='The new password - at least 8 characters, 1 number, 1 special symbol'),
        'password_confirm': fields.String(required=True, description='The new password'),
    })

    model_change_password = api.model('change_password', {
        'old_password': fields.String(required=True, description='Current password'),
        'password': fields.String(required=True, description='The new password - at least 8 characters, 1 number, 1 special symbol'),
        'password_confirm': fields.String(required=True, description='Confirm the new password'),
    })

    message_response = api.model('response', {
        'message': fields.String(required=True, description='')
    })

    model_send_OTP_phone = api.model('send_OTP_phone', {
        'phone_number': fields.String(required=True, description='The phone number for OTP'),
    })

    model_change_phone_number = api.model('change_phone_number', {
        'phone_number': fields.String(required=True, description='The phone number for change'),
        'code': fields.String(required=True, description='The OTP code sent through SMS'),
    })

    model_switch_role = api.model('switch_role', {
        'role': fields.String(required=True, description='Current role. Must be either user or organization'),
        'organization_id': fields.String(required=False, description='The ID of current organization. Must be specified when role is set to organization'),
    })