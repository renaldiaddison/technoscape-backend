from django.core.mail import EmailMultiAlternatives
from django.forms.utils import ErrorDict
from django.template.loader import get_template
from dotenv import load_dotenv
import os
import pathlib
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError
load_dotenv()


def get_env(key):
    return os.environ.get(key)


def send_user_activation_email(to, activation_link_param):
    activation_link = get_env('ACTIVATION_LINK_PATH') + activation_link_param

    email_html = get_template('activation_user_email.html')
    data = {'activation_link_url': activation_link}

    subject, from_email, to = 'Account Activation', get_env(
        'EMAIL_HOST_USER'), to
    html_content = email_html.render(data)
    msg = EmailMultiAlternatives(
        subject=subject, from_email=from_email, to=[to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def validate_birthdate_format(value):
    if not value.isdigit() or len(value) != 8:
        raise ValidationError(
            'Invalid birthdate format. Please use "ddmmyyyy".')

    day = int(value[:2])
    month = int(value[2:4])
    year = int(value[4:])

    if day < 1 or day > 31:
        raise ValidationError('Invalid day in the birthdate.')
    if month < 1 or month > 12:
        raise ValidationError('Invalid month in the birthdate.')
    if year < 1900:
        raise ValidationError(
            'Invalid year in the birthdate. Must be at least 1900.')


def validate_gender(value):
    if value not in ('0', '1'):
        raise ValidationError(
            'Invalid gender value. Use "0" for male or "1" for female.')


def get_first_error(error_dict: ErrorDict):
    for key, value in error_dict.items():
        if isinstance(value, list) and len(value) > 0:
            return __capitalize_first_character(key) + ": " + value[0].title()
    return None, None


def __capitalize_first_character(input_string: str):
    return input_string[0].capitalize() + input_string[1:]


def get_directory(relative_path):
    current_dir = os.getcwd()
    return os.path.join(current_dir, relative_path)


class CurrencyConverter:
    exchange_rate_idr_to_usd = 0.000066

    @classmethod
    def idr_to_usd(cls, amount_in_idr):
        return amount_in_idr * cls.exchange_rate_idr_to_usd
    
    @classmethod
    def usd_to_idr(cls, amount_in_usd):
        return amount_in_usd / cls.exchange_rate_idr_to_usd
