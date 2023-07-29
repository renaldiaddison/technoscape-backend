from rest_framework import serializers
from django.core.validators import RegexValidator
from utils import utils, responses
from .models import User, UserApproval
import requests
from django.utils import timezone


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
            'pin': {'write_only': True},
            'uid': {'read_only': True}
        }

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

    @classmethod
    def get_user_profile(cls, access_token):
        url_suffix = "/user/info"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        return response

    @classmethod
    def get_user_bank_account(cls, access_token):
        url_suffix = "/bankAccount/info/all"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix

        payload = {}
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        return response

    @classmethod
    def get_bank_account_info(cls, access_token, accountNo):
        url_suffix = "/bankAccount/info/"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix

        payload = {
            'accountNo': accountNo
        }
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        return response

    @classmethod
    def get_bank_account_info(cls, access_token, accountNo):
        url_suffix = "/bankAccount/info/"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix

        payload = {
            'accountNo': accountNo
        }
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        return response

    @classmethod
    def register(cls, ktpId, username, loginPassword, phoneNumber, birthDate, gender, email):
        url_suffix = "/user/auth/create"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix
        payload = {
            "ktpId": ktpId,
            "username": username,
            "loginPassword": loginPassword,
            "phoneNumber": phoneNumber,
            "birthDate": birthDate,
            "gender": gender,
            "email": email
        }
        headers = {}
        response = requests.post(url, headers=headers, json=payload)

        return response

    @classmethod
    def create_transaction(cls, senderAccountNo, receiverAccountNo, amount, access_token):
        url_suffix = "/bankAccount/transaction/create"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix
        payload = {
            "senderAccountNo": senderAccountNo,
            "receiverAccountNo": receiverAccountNo,
            "amount": amount
        }
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.post(url, headers=headers, json=payload)

        return response

    @classmethod
    def get_transaction(cls, accountNo, pageNumber, access_token, traxType=["TRANSFER_IN", "TRANSFER_OUT"], recordsPerPage=2):
        url_suffix = "/bankAccount/transaction/info"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix
        payload = {
            "accountNo": accountNo,
            "traxType": traxType,
            "pageNumber": pageNumber,
            "recordsPerPage": recordsPerPage,
        }

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.post(url, headers=headers, json=payload)

        return response


class UserApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApproval
        fields = '__all__'

    # def create(self, validated_data):
    #     validated_data['income'] = utils.CurrencyConverter.idr_to_usd(
    #         validated_data['income'])
    #     validated_data['coappliciant_income'] = utils.CurrencyConverter.idr_to_usd(
    #         validated_data['coappliciant_income'])
    #     return super().create(validated_data)


class ImportantUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['old_password', 'current_password', 'pin', 'is_approved']


class UpdatePasswordUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['current_password']
