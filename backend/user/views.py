from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils import utils, responses
from .models import User
from .serializers import UserSerializer
import requests


class __CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            responses.error_response(
                error_message=utils.get_first_error(serializer.errors))

        json_register_response = UserSerializer.register(serializer.validated_data['ktpId'], serializer.validated_data['username'], serializer.validated_data['loginPassword'],
                                                         serializer.validated_data['phoneNumber'], serializer.validated_data['birthDate'], serializer.validated_data['gender'], serializer.validated_data['email']).json()
        if not json_register_response.get('success'):
            return responses.error_response(error_message=json_register_response.get('errMsg'))

        User.objects.create(uid=json_register_response.get('data').get(
            'uid'), pin=serializer.validated_data['pin'])

        create_new_account_response = UserSerializer.create_new_account(
            serializer.validated_data['username'], serializer.validated_data['loginPassword'])
        json_create_new_account_response = create_new_account_response.json()

        if not json_create_new_account_response.get('success'):
            return responses.error_response(error_message=json_create_new_account_response.get('errMsg'))

        response_data = dict(serializer.validated_data)
        response_data['uid'] = json_register_response.get('data').get('uid')

        return responses.success_response(data=response_data)


class __LoginUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        loginPassword = request.data.get('loginPassword')

        json_login_response = UserSerializer.login(
            username=username, loginPassword=loginPassword).json()

        if not json_login_response.get('success'):
            return responses.error_response(error_message=json_login_response.get('errMsg'))

        accessToken = json_login_response.get('data').get('accessToken')

        json_get_user_profile_response = UserSerializer.get_user_profile(
            accessToken).json()

        if not json_get_user_profile_response.get('success'):
            return responses.error_response(error_message=json_get_user_profile_response.get('errMsg'))

        json_get_user_profile_response.get('data')['accessToken'] = accessToken

        return responses.success_response(data=json_get_user_profile_response.get('data'))


class __GetUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        json_get_user_profile_response = UserSerializer.get_user_profile(
            access_token).json()

        if not json_get_user_profile_response.get('success'):
            return responses.error_response(error_message=json_get_user_profile_response.get('errMsg'))

        return responses.success_response(data=json_get_user_profile_response.get('data'))


class __GetUserBankAccount(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        json_get_user_bank_account_response = UserSerializer.get_user_bank_account(
            access_token).json()

        if not json_get_user_bank_account_response.get('success'):
            return responses.error_response(error_message=json_get_user_bank_account_response.get('errMsg'))

        bank_account_data = json_get_user_bank_account_response.get(
            'data').get('accounts')[0]

        return responses.success_response(data=bank_account_data)
    

create_user_api_view = __CreateUserAPIView.as_view()
login_user_api_view = __LoginUserAPIView.as_view()
get_user_api_view = __GetUserAPIView.as_view()
get_user_bank_account_view = __GetUserBankAccount.as_view()
