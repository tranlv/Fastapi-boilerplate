import re
from datetime import datetime, timedelta
import phonenumbers
from password_strength import PasswordPolicy


def is_valid_phone_number(phone_number):

    try:
        phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(phone_number)
    except Exception as e:
        print(e.__str__())
        return False


def is_valid_password(password):
    try:
        policy = PasswordPolicy.from_names(
            length=8, uppercase=0, numbers=0, special=0, nonletters=0,)
        return True if len(policy.test(password)) == 0 else False
    except Exception as e:
        print(e.__str__())
        return False


def is_valid_email(email):

    try:
        regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.search(regex, email) is not None
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
