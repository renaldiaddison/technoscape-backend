from django.core.mail import EmailMultiAlternatives
from django.forms.utils import ErrorDict
from django.template.loader import get_template
from dotenv import load_dotenv
import os
import pathlib
import uuid
from django.utils import timezone
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