#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request

# own modules
from app.modules.auth.auth_controller import AuthController
from app.modules.auth.auth_dto import AuthDto
from app.extensions.utils.decorator import token_required
from app.extensions.view import Resource

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AuthDto.api

##### EMAIL REGISTRATION #####
@api.route('/register', methods=['POST'])
class Register(Resource):

    @api.expect(AuthDto.model_email_pasword_registration)
    def post(self):
        """Create new user with email and password"""

        return AuthController().register_using_email_password(request.json)


@api.route('/confirm', methods=['POST'])
class ConfirmationEmail(Resource):
    @api.expect(AuthDto.model_email_pasword_registration_confirm)
    def post(self):
        """Validate confirmation code sent to email for registration"""

        return AuthController().confirm_email_code_for_registration(request.json)


##### RESET PASSWORD BY MAIL #####
@api.route('/password-reset-email', endpoint='password_reset_email', methods=['POST'])
class PasswordResetEmail(Resource):

    @api.expect(AuthDto.model_password_reset_email)
    def post(self):
        """Request password reset with email without using old password"""

        return AuthController().reset_password_by_email_without_old_password(request.json)


@api.route('/password-reset-email-confirm', endpoint='password_reset_email_confirm', methods=['POST'])
class PasswordResetEmailConfirm(Resource):
    @api.expect(AuthDto.model_password_reset_email_confirm)
    def post(self):
        """Validate confirmation token sent to email for password reset"""

        return AuthController().confirm_email_token_for_reset_password(request.json)


##### CHANGE PASSWORD BY MAIL AND OLD PASSWORD #####
@api.route('/change-password', methods=['POST'])
class ChangePassword(Resource):

    @api.expect(AuthDto.model_change_password)
    def post(self):
        """Change password request using old password"""

        return AuthController().change_password_using_old_password(request.json)


##### EMAIL/PASS LOGIN #####
@api.route('/login', methods=['POST'])
class Login(Resource):

    @api.expect(AuthDto.model_login)
    def post(self):
        """Login user using email and password"""

        return AuthController().login_using_email_password(request.json)


##### SOCIAL LOGIN#####
@api.route('/social_login/google', methods=['POST'])
class GoogleLogin(Resource):

    @api.expect(AuthDto.model_social_login)
    def post(self):
        """Create or Login user with Google Account"""

        return AuthController().login_using_oath2_google(request.json)

        
@api.route('/social_login/facebook', methods=['POST'])
class FacebookLogin(Resource):

    @api.expect(AuthDto.model_social_login)
    def post(self):
        """Create or Login user with FB Account"""

        return AuthController().login_using_oath2_facebook(request.json)


##### SMS REGISTRATION #####
@api.route('/sms/register', methods=['POST'])
class SmsRegister(Resource):

    @api.expect(AuthDto.model_sms_register)
    def post(self):
        """Register using phone number and password"""
        
        return AuthController().register_using_phone_password(request.json)


@api.route('/sms/confirm', methods=['POST'])
class SmsConfirm(Resource):

    @api.expect(AuthDto.model_confirm_sms)
    def post(self):
        """Validate confirmation code sent to sms for mobile registration"""

        return AuthController().confirm_sms_code_for_registration(request.json)

##### SMS LOGIN WITH PASSWORD#####
@api.route('/sms/login_password', methods=['POST'])
class SmsLoginPassword(Resource):

    @api.expect(AuthDto.model_sms_login_with_password)
    def post(self):
        """Login with phone number and password."""

        return AuthController().login_using_phone_password(request.json)


##### SMS LOGIN WITH CODE#####
@api.route('/sms/login_code', methods=['POST'])
class SmsLoginCode(Resource):

    @api.expect(AuthDto.model_sms_login_with_code)
    def post(self):
        """Login using phone number and sent a code to valid phone number"""
        
        return AuthController().login_using_phone_code(request.json)


@api.route('/sms/login_code/confirm', methods=['POST'])
class SmsLoginCodeConfirm(Resource):

    @api.expect(AuthDto.model_sms_login_with_code_confirm)
    def post(self):
        """Validate code send to phone number for mobile login"""

        return AuthController().confirm_sms_code_for_login(request.json)


##### RESET PASSWORD USING PHONE #####
@api.route('/password-reset-phone', methods=['POST'])
class PasswordResetPhone(Resource):

    @api.expect(AuthDto.model_reset_password_phone)
    def post(self):
        """Request password reset with phone code"""

        return AuthController().reset_password_by_phone_code(request.json)


@api.route('/password-reset-phone-confirm', methods=['POST'])
class PasswordResetPhoneConfirm(Resource):

    @api.expect(AuthDto.model_reset_password_phone_confirm)
    def post(self):
        """Validate phone code for password reset using phone number"""

        return AuthController().confirm_phone_code_for_reset_password(request.json)

##### Change phone number #####
@api.route('/change-phone-number', methods=['POST'])
class ChangePhoneNumber(Resource):

    @api.expect(AuthDto.model_change_phone_number)
    def post(self):
        """Change phone number for logged-in user"""

        return AuthController().change_phone_number_confirm(request.json)


##### RESET OTP CODE #####
@api.route('/send-OTP', methods=['POST'])
class SendOTPPhone(Resource):

    @api.expect(AuthDto.model_send_OTP_phone)
    def post(self):
        """Send OTP to phone number"""

        return AuthController().send_OTP(request.json)

##### INPUT NEW PASSWORD AFTER RECEIVING CODE ####
@api.route('/change-password-token', methods=['POST'])
class ChangePasswordByToken(Resource):

    @api.expect(AuthDto.model_change_password_token)
    def post(self):
        """Change password using reset token"""
        
        return AuthController().input_new_password_using_code(request.json)


##### OTHERS#######
@api.route('/logout', methods=['POST'])
class Logout(Resource):

    @token_required
    def post(self):
        """Logout user and blacklist token"""

        return AuthController().logout_user()


@api.route('/switch-role', methods=['POST', 'GET'])
class UserSwitchRole(Resource):
    @token_required
    @api.expect(AuthDto.model_switch_role)
    def post(self):
        """ Switch role to user or organization (with organization_id)"""

        data = api.payload
        return AuthController().switch_role(data)

    @token_required
    @api.response(code=200, model=AuthDto.model_switch_role, description='')
    def get(self):
        """ Get current role"""

        controller = AuthController()
        return controller.get_current_role()


#### TODO -  Currently not using these API ###
#@api.route('/sms/resend_confirm', methods=['POST'])
class SmsResendConfirm(Resource):

    @api.expect(AuthDto.model_resend_confirmation_sms)
    def post(self):
        """ Resend confirmation sms code."""

        post_data = request.json
        return AuthController().resend_confirmation_sms(post_data)

#@api.route('/resend_confirmation', methods=['POST'])
class ResendConfirmation(Resource):

    @api.expect(AuthDto.model_login)
    def post(self):
        """Resend confirmation email"""

        data = api.payload
        return AuthController().resend_confirmation(data=data)
