#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from datetime import datetime

# third-party modules
from flask.templating import render_template
import requests
from flask import g
from flask_restx import marshal

# own modules
from app.extensions.db import db
from app.extensions import messages
from app.config import BaseConfig as Config
from app.extensions.models.ban import UserBan
from app.extensions.models.user import SocialAccount, User
from app.extensions.models.organization import Organization
from app.extensions.utils.response import send_error, send_result
from app.extensions.utils.util import (is_valid_password, is_valid_display_name, is_valid_phone_code, confirm_token, decode_base64_jwt_payload, encode_auth_token,
                               generate_confirmation_token, is_valid_email, send_confirmation_email, send_email, send_password_reset_email,
                               send_verification_sms, is_valid_phone_number, create_random_string)
from app.extensions.es import get_model as es_get_model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AuthController:

    ##### EMAIL REGISTRATION #####
    def register_using_email_password(self, data):

        if not isinstance(data, dict):
            return send_error(
                message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('email'))
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password'))
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password_confirm'))
        
        if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('display_name'))
        
        if not 'is_policy_accepted' in data or str(data['is_policy_accepted']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_POLICY_ACCEPTED)

        if data['password_confirm'] != data['password']:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)

        email = data['email'].strip()
        display_name = data['display_name'].strip()
        password = data['password'].strip()
       
        if is_valid_email(email) is False:
            return send_error(message=messages.ERR_INVALID_EMAIL)

        if is_valid_password(password) is False:
            return send_error(message=messages.ERR_INVALID_PASSWORD)

        if is_valid_display_name(display_name) is False:
            return send_error(message=messages.ERR_INVALID_DISPLAY_NAME)    
  
        banned = UserBan.query.filter(UserBan.ban_by == email).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)

        if is_display_name_already_existed(display_name) is True:
            return send_error(message=messages.ERR_DISPLAY_NAME_EXISTED)

        user = User.get_user_by_email(email=email)
        if user is not None:
            if user.confirmed is False:
                send_confirmation_email(to=user.email, user=user)
            return send_result()
 
        try:
            user = create_user_helper(data)
            send_confirmation_email(to=user.email, user=user)
            return send_result()
                
        except Exception as e:
            print(e.__str__())
            db.session.rollback()            
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def confirm_email_code_for_registration(self, data):

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'token' in data or str(data['token']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('token'))

        token = data['token']

        email = confirm_token(token, expirations=1800)
        if email is None or email.strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_CODE)

        if is_valid_email(email) is False:
            return send_error(message=messages.ERR_INVALID_EMAIL)

        user = User.get_user_by_email(email=email)
        if user is not None and user.confirmed is True:
            return send_result()

        if user is None:
            return send_error(message=messages.ERR_INVALID_CODE)

        try:
            user.confirmed = True
            user.email_confirmed_at = datetime.now()

                #TODO send request to update user in search
                #user_dsl = ESUser(_id=user.id, display_name=user.display_name, email=user.email, gender=user.gender, age=user.age, reputation=user.reputation, first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name)
                #user_dsl.save()


            
            db.session.commit()
            html = render_template('welcome.html', user=user)
            send_email(user.email, 'Hoovada - Chào mừng bạn tham gia vào cộng đồng!', html)
            return send_result()
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    
    ##### RESET PASSWORD BY MAIL #####
    def reset_password_by_email_without_old_password(self, data):
        """Reset password without old password- Send password reset confirmation link to email if account exits"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('email'))

        if is_valid_email(data['email']) is False:
            return send_error(message=messages.ERR_INVALID_EMAIL)

        email = data['email']
        user = User.get_user_by_email(email)
        # just send success so that attacker wont know whether account already existed
        if user is None:
            return send_result()

        try:
            send_password_reset_email(to=email)
            return send_result()
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def confirm_email_token_for_reset_password(self, data):
        """Reset password confirmation after link on email is clicked"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'token' in data or str(data['token']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('token'))
        
        token = data['token']
        email = confirm_token(token)
        if email is None or email.strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_CODE)

        if is_valid_email(email) is False:
            return send_error(message=messages.ERR_INVALID_EMAIL)   

        user = User.query.filter_by(email=email).first()
        if not user:
             # just send success so that attacker wont know whether account already existed
            return send_result()

        return send_result(data={'reset_token':token})


    ##### CHANGE PASSWORD BY MAIL AND OLD PASSWORD #####
    def change_password_using_old_password(self, data):
        """Change password for current user using old password"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password'))
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password_confirm'))

        if data['password_confirm'] != data['password']:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)

        if not 'old_password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('old_password'))

        old_password = data['old_password'].strip()
        password = data['password'].strip()
        if is_valid_password(password) is False:
            return send_error(message=messages.ERR_INVALID_PASSWORD)

        user = g.current_user
        if user.check_password(old_password) is False:
            return send_error(message=messages.ERR_INCORRECT_EMAIL_OR_PASSWORD)

        try:
            user.set_password(password=password)

            # confirm password right here
            if user.confirmed is False:
                user.confirmed = True
                user.email_confirmed_at = datetime.now()

            db.session.commit()
            return send_result()
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    ##### EMAIL/PASS login #####
    def login_using_email_password(self, data):

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password'))

        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('email'))

        email = data['email'].strip()
        password = data['password'].strip()

        banned = UserBan.query.filter(UserBan.ban_by == email).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)

        # either email or password wrong
        user = User.get_user_by_email(email)
        if user is None:
            return send_error(message=messages.ERR_INCORRECT_EMAIL_OR_PASSWORD) 
        if user.check_password(password) is False:
            return send_error(message=messages.ERR_INCORRECT_EMAIL_OR_PASSWORD)      

        try:
            if user.confirmed is False:
                send_confirmation_email(to=user.email, user=user)
                return send_error(message=messages.ERR_ACCOUNT_NOT_EXISTED_CONFIRMED)
            
            # activate when user re-login
            user.is_deactivated = False
            db.session.commit()
            auth_token = encode_auth_token(user=user)
            if auth_token:
                return send_result(data={'access_token': auth_token})

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_FAILED_LOGIN)


    ##### SOCIAL LOGIN#####
    def login_using_oath2_google(self, data):
        """Log in to google and create account if not existed"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'access_token' in data or str(data['access_token']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('access_token'))
        
        access_token = str(data['access_token'])

        try:
            resp = requests.get(Config.GOOGLE_PROFILE_URL, params={'access_token': access_token, 'alt': 'json'})
            resp.raise_for_status()
            extra_data = resp.json()
            user = save_social_account('google', extra_data)
        
            auth_token = encode_auth_token(user=user)
            if auth_token:
                return send_result(data={'access_token': auth_token})

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_LOGIN_FAILED.format(e))


    def login_using_oath2_facebook(self, data):
        """Log in to google and create account if not existed"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'access_token' in data or str(data['access_token']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('access_token'))

        access_token = str(data['access_token'])

        try:
            resp = requests.get(
                Config.GRAPH_API_URL,
                params={
                    'fields': ','.join(Config.FACEBOOK_FIELDS),
                    'access_token': access_token,
                })

            resp.raise_for_status()
            extra_data = resp.json()
            user = save_social_account('facebook', extra_data)
        
            auth_token = encode_auth_token(user=user)
            if auth_token:
                return send_result(data={'access_token': auth_token})
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_LOGIN_FAILED.format(e))


    ##### SMS REGISTRATION #####
    def register_using_phone_password(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('display_name'))

        if not 'is_policy_accepted' in data or str(data['is_policy_accepted']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_POLICY_ACCEPTED)

        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password'))
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password_confirm'))

        if data['password_confirm'] != data['password']:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))

        password = data['password'].strip()
        phone_number = data['phone_number']
        display_name = data['display_name']

        if is_valid_password(password) is False:
            return send_error(message=messages.ERR_INVALID_PASSWORD)

        if is_display_name_already_existed(display_name) is not None:
            return send_error(message=messages.ERR_DISPLAY_NAME_EXISTED)

        if is_valid_display_name(display_name) is False:
            return send_error(message=messages.ERR_INVALID_DISPLAY_NAME)        
        
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        try:
            banned = UserBan.query.filter(UserBan.ban_by == phone_number).first()
            if banned:
                raise send_error(message=messages.ERR_BANNED_ACCOUNT)
            
            # Check user by phone, does not do anything if account already existed or send confirm code
            user = User.get_user_by_phone_number(phone_number)
            if user is not None:
                if user.confirmed is False:
                    code = send_verification_sms(phone_number, user)
                    if code is None:
                        return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)               
                return send_result()

            user = User(display_name=display_name, phone_number=phone_number, confirmed=False)
            user.set_password(password=password)
            db.session.add(user)

            code = send_verification_sms(phone_number, user)
            if code is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

            db.session.commit()
            return send_result()
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

       
    def confirm_sms_code_for_registration(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('code'))

        phone_number = data['phone_number']
        code = data['code']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

        if user is not None and user.confirmed is True:
            return send_result()

        if is_valid_phone_code(phone_number, code, user) is False:
            return send_error(message=messages.ERR_INVALID_CODE)

        try:
            user.confirmed = True
            user.verification_sms_time = datetime.now()

            #user_dsl = ESUser(_id=user.id, display_name=user.display_name, email=user.email, gender=user.gender, age=user.age, reputation=user.reputation, first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name)
            #user_dsl.save()

            db.session.commit()
            html = render_template('welcome.html', user=user)
            send_email(user.email, 'Hoovada - Chào mừng bạn tham gia vào cộng đồng!', html)
            return send_result()
                
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))        

  
    ##### SMS LOGIN #####
    def login_using_phone_password(self, data):
        """ Login using phone number and password"""

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))

        phone_number = data['phone_number']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        banned = UserBan.query.filter(UserBan.ban_by == data['phone_number']).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)
            
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

        try:
            if user.check_password(data['password']):
                if user.confirmed is False:
                    code = send_verification_sms(phone_number, user)
                    if code is None:
                        return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)  
                    return send_error(message=messages.ERR_ACCOUNT_NOT_EXISTED_CONFIRMED)
                
                user.is_deactivated = False
                db.session.commit()
                auth_token = encode_auth_token(user=user)
                if auth_token:
                    return send_result(data={'access_token': auth_token})
                    
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_LOGIN_FAILED.format(e))


    ##### SMS LOGIN WITH CODE#####
    def login_using_phone_code(self, data):
        """ Login using phone number and then sent a code to valid phone number"""

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))

        phone_number = data['phone_number']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        banned = UserBan.query.filter(UserBan.ban_by == phone_number).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)
        
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

        if user.confirmed is False:
            code = send_verification_sms(phone_number, user)
            if code is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER) 
            return send_error(message=messages.ERR_ACCOUNT_NOT_EXISTED_CONFIRMED)
         
        try:
            code = send_verification_sms(phone_number, user)
            if code is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)
            
            return send_result()
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_LOGIN_FAILED.format(e))

    def confirm_sms_code_for_login(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('code'))
        
        phone_number = data['phone_number']
        code = data['code']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

        if user.confirmed is False:
            code = send_verification_sms(phone_number, user)
            if code is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)  
            return send_error(message=messages.ERR_ACCOUNT_NOT_EXISTED_CONFIRMED)

        if is_valid_phone_code(phone_number, code, user) is False:
            return send_error(message=messages.ERR_INVALID_CODE)

        try: 
            user.is_deactivated = False
            db.session.commit()
            auth_token = encode_auth_token(user=user)
            if auth_token:
                return {'access_token': auth_token}
            
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_LOGIN_FAILED.format(e))


    ##### RESET OTP CODE #####
    def send_OTP(self, data):
        """Reset password request by SMS OTP"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))

        phone_number = data['phone_number']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        try:
            user = User.get_user_by_phone_number(phone_number)
            if user is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

            code = send_verification_sms(phone_number, user)
            if code is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

            return send_result()

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    ##### RESET PASSWORD USING PHONE #####
    def reset_password_by_phone_code(self, data):
        """Reset password request by SMS OTP"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT) 
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))

        phone_number = data['phone_number']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)      
        
        try:
            user = User.get_user_by_phone_number(phone_number)
            if user is None:
                return send_result()

            code = send_verification_sms(phone_number, user)
            if code is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

            return send_result()
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))  


    def confirm_phone_code_for_reset_password(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))

        phone_number = data['phone_number']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('code'))
        
        code = data['code']

        try:
            user = User.get_user_by_phone_number(phone_number)
            if user is None:
                return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)

            if is_valid_phone_code(phone_number, code, user) is False:
                return send_error(message=messages.ERR_INVALID_CODE)

            return send_result(data={'reset_token':generate_confirmation_token(phone_number)}, message=messages.MSG_PASS_INPUT_PROMPT)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))    

    ##### INPUT NEW PASSWORD AFTER RECEIVING CODE ####
    def input_new_password_using_code(self, data):

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'reset_token' in data or str(data['reset_token']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('reset_token'))

        if not 'token_type' in data or str(data['token_type']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('token_type'))
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password_confirm'))
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('password'))

        token_type = data['token_type']
        token = data['reset_token']
        password_confirm = data['password_confirm']
        password = data['password']

        if password != password_confirm:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)
            
        if is_valid_password(password) is False:
            return send_error(message=messages.ERR_INVALID_PASSWORD)

        if token_type == 'email':
            email = confirm_token(token)
            if email is None or email.strip().__eq__(''):
                return send_error(message=messages.ERR_INVALID_CODE)
            user = User.get_user_by_email(email)
        else:
            phone_number = confirm_token(token)
            user = User.get_user_by_phone_number(phone_number)

        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_EXISTED_CONFIRMED)        

        try:
            user.set_password(password=password)
            db.session.commit()
            return send_result()

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))    


    ##### Change phone number #####
    def change_phone_number_confirm(self, data):
        """Change phone number for current user"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if code not in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('code'))

        if phone_number not in data:
            return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)
        
        code = data.get('code')
        phone_number = data.get('phone_number')
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)
            
        user = g.current_user
        if is_valid_phone_code(phone_number, code, user) is False:
            return send_error(message=messages.ERR_INVALID_CODE)

        try:
            user.phone_number = phone_number
            db.session.commit()
            return send_result()
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    ##### logout ####
    def logout_user(self, request):

        auth_token = None
        if 'X-Hoovada-Jwt' in request.headers:
            auth_token = request.headers['X-Hoovada-Jwt']
        else:
            return send_result()
        
        try:  
            user_id = decode_base64_jwt_payload(auth_token)
            user = User.get_user_by_id(int(user_id))
            if user is None:
                return send_result()

            user.last_seen = datetime.now()
            db.session.commit()
            return send_result()
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_LOGOUT_FAILED.format(str(e)))

    
    def switch_role(self, data):
        if 'role' not in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('a role'))
        if 'role' in data and data['role'] not in ['user','organization']:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('a role in list (user, organization)'))
        if 'role' in data and data['role'] == 'organization' and 'organization_id' not in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('organization_id when role is organization'))
        if 'role' in data:
            session['role'] = data['role']
            if data['role'] == 'user' and 'organization_id' in session:
                del session['organization_id']
        if 'organization_id' in data and data['role'] == 'organization':
            session['organization_id'] = data['organization_id']
            org = Organization.query.filter_by(id=data['organization_id']).first()
            if org is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Organization',data['organization_id']))
            if org.user_id != g.current_user.id:
                return send_error(message=messages.ERR_NOT_AUTHORIZED)
        return send_result()
    

    def get_current_role(self):
        return send_result(data={'role': session['role'], 'organization_id': None if 'organization_id' not in session else session['organization_id']})


    ########### CURRENTLY UNUSED ########
    def resend_confirmation(self, data):

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('email'))

        if is_valid_email(data['email']) is False:
            return send_error(message=messages.ERR_INVALID_EMAIL)

        email = data['email'].strip()
        user = User.get_user_by_email(email=email)
        if not user:
            return send_error(message=messages.ERR_INCORRECT_EMAIL_OR_PASSWORD)

        # if already activated, do not send confirm email
        if user.confirmed is True:
            return send_result()        
        
        try:
            send_confirmation_email(to=email, user=user)
            return send_result()
            
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    
    def resend_confirmation_sms(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))
        
        phone_number = data['phone_number']
        if is_valid_phone_number(phone_number) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_INCORRECT_PHONE_NUMBER)
        
        try:
            code = send_verification_sms(phone_number, user)
            if code is not None:
                return send_result()
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))
            

def is_display_name_already_existed(display_name):
    """ Check user exist by its user_name. Return True is existed else return False if not existed"""

    user = User.query.filter_by(display_name=display_name).first()
    return True if user is not None else False


def create_unique_display_name(display_name):
    """ Create a unique user_name, if it exists in DB we will add "_1", "_2"... until it not exists in DB"""

    unique_display_name = display_name
    count = 0
    while is_display_name_already_existed(unique_display_name) is True:
        count += 1
        unique_display_name = display_name + '_' + str(count)

    return unique_display_name


def create_user_helper(data):
    try: 
        email = data.get('email')
        phone_number = data.get('phone_number')

        if email is None and phone_number is None:
            raise Exception(messages.ERR_PLEASE_PROVIDE.format('email or mobile'))

        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        middle_name = data.get('middle_name', None)
        display_name =  data.get('display_name')
        password = data.get('password', create_random_string(8))
        confirmed = data.get('confirmed', False)

        user = User(display_name=display_name, email=email, confirmed=confirmed, first_name=first_name, middle_name=middle_name, last_name=last_name)
        user.set_password(password=password)
        
        if email is not None and confirmed is True:
            user.email_confirmed_at = datetime.now()
        
        if phone_number is not None and confirmed is True:
            user.verification_sms_time = datetime.now()

        db.session.add(user)
        db.session.commit()
        return user

    except Exception as e:
        db.session.rollback()
        print(e.__str__())

        if email is not None:
            user = db.session.query(User).filter(User.email == email)
        else:
            user = db.session.query(User).filter(User.phone_number == phone_number)
        if user is not None:
            db.session.delete(user)
            db.session.commit()

        raise e


def save_social_account(provider, data):

    if not 'email' in data and 'user_mobile_phone' not in data:
        return send_error(message=messages.ERR_PLEASE_PROVIDE.format('email or mobile'))

    using_email = True
    entity = None
    if 'email' in data:
        if is_valid_email(data['email']) is False:
            return send_error(message=messages.ERR_INVALID_EMAIL)
        entity = data['email']

    elif 'user_mobile_phone' in data:
        entity = data['user_mobile_phone']
        data['phone_number'] = data['user_mobile_phone'] # we use phone_number in DB
        using_email = False

        if is_valid_phone_number(entity) is False:
            return send_error(message=messages.ERR_INVALID_NUMBER)

    banned = UserBan.query.filter(UserBan.ban_by == entity).first()
    if banned is not None:
        raise Exception(messages.ERR_BANNED_ACCOUNT)

    try:
        user = User.get_user_by_email(entity) if using_email is True else User.get_user_by_phone_number(entity)
        if not user:
            display_name = data.get('name', entity).strip()
            display_name = create_unique_display_name(display_name)
            if is_valid_display_name(display_name) is False:
                display_name = entity

            data['display_name'] = display_name
            data['confirmed'] = True

            user = create_user_helper(data)
            
            #TODO send request to update user in search
            #user_dsl = ESUser(_id=user.id, display_name=user.display_name, email=user.email, gender=user.gender, age=user.age, reputation=user.reputation, first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name)
            #user_dsl.save()

        user.is_deactivated = False
        social_account = SocialAccount.query.filter_by(uid=data['id']).first()
        if social_account is None:            
            social_account = SocialAccount(provider=provider, uid=data['id'], extra_data=json.dumps(data), user_id=user.id)
            db.session.add(social_account)

        if social_account.user_id != user.id:
            social_account.user_id = user.id

        db.session.commit()
        return user

    except Exception as e:
        print(e.__str__())
        raise e      
