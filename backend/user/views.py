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

        url_suffix = "/user/auth/create"
        url = utils.get_env('HACKATHON_API_PREFIX') + url_suffix
        payload = {
            "ktpId": serializer.validated_data['ktpId'],
            "username": serializer.validated_data['username'],
            "loginPassword": serializer.validated_data['loginPassword'],
            "phoneNumber": serializer.validated_data['phoneNumber'],
            "birthDate": serializer.validated_data['birthDate'],
            "gender": serializer.validated_data['gender'],
            "email": serializer.validated_data['email']
        }
        headers = {}
        response = requests.post(url, headers=headers, json=payload)
        json_response = response.json()
        if not json_response.get('success'):
            return responses.error_response(error_message=json_response.get('errMsg'))

        User.objects.create(uid=json_response.get('data').get(
            'uid'), pin=serializer.validated_data['pin'])

        create_new_account_response = UserSerializer.create_new_account(
            serializer.validated_data['username'], serializer.validated_data['loginPassword'])
        json_create_new_account_response = create_new_account_response.json()

        if not json_create_new_account_response.get('success'):
            return responses.error_response(error_message=json_create_new_account_response.get('errMsg'))

        return responses.success_response(data=serializer.validated_data)


create_user_api_view = __CreateUserAPIView.as_view()
