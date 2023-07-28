from rest_framework import serializers
from django.core.validators import RegexValidator
from utils import utils
from .models import User
import requests


class UserSerializer(serializers.ModelSerializer):
    ktpId = serializers.CharField(validators=[RegexValidator(
        r'^\d+$', message='Only digits are allowed.')],)
    username = serializers.CharField()
    loginPassword = serializers.CharField()
    phoneNumber = serializers.CharField(validators=[RegexValidator(
        r'^\d+$', message='Only digits are allowed.')],)
    birthDate = serializers.CharField(
        max_length=8,
        validators=[utils.validate_birthdate_format])
    gender = serializers.CharField(max_length=1, validators=[RegexValidator(
        r'^\d+$', message='Only digits are allowed.'),
        utils.validate_gender],)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['uid', 'ktpId', 'username', 'loginPassword', 'gender',
                  'phoneNumber', 'birthDate', 'email', 'pin', 'role']
        extra_kwargs = {
            'loginPassword': {'write_only': True},
            "pin": {'write_only': True},
            'uid': {'read_only': True}
        }

    def create(self, validated_data, uid):
        validated_data['uid'] = uid
        return super().create(validated_data)

    @classmethod
    def login(cls, username, loginPassword):
        url_suffix = "/user/auth/token"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix

        payload = {
            "username": username,
            "loginPassword": loginPassword
        }
        headers = {}

        response = requests.request("POST", url, headers=headers, json=payload)

        return response

    @classmethod
    def create_new_account(cls, username, loginPassword):
        login_response = cls.login(username, loginPassword)
        json_login_response = login_response.json()

        if not json_login_response.get('success'):
            return login_response

        url_suffix = "/bankAccount/create"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix

        payload = {
            "balance": 0
        }

        authorization = 'Bearer ' + \
            json_login_response.get('data').get('accessToken')

        headers = {
            'Authorization': authorization
        }

        response = requests.request(
            "POST", url, headers=headers, json=payload)

        return response
