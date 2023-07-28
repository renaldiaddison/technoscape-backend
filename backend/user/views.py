from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils import utils
from .models import User
from .serializers import UserSerializer
import requests
import eventlet
eventlet.monkey_patch()


class __CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"data": {},
                             "errMsg": utils.get_first_error(serializer.errors)
                             }, status=status.HTTP_200_OK)

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
            return Response({"data": {},
                             "success": False,
                             "errMsg": json_response.get('errMsg')
                             }, status=status.HTTP_200_OK)

        User.objects.create(uid=json_response.get('data').get(
            'uid'), pin=serializer.validated_data['pin'])
        serializer.create_new_account()
        return Response({"data": {}, "success": True}, status=status.HTTP_200_OK)


create_user_api_view = __CreateUserAPIView.as_view()
