from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils import utils, responses
from .models import User
from .serializers import UserSerializer, UserApprovalSerializer
import requests


class __CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            responses.error_response(
                error_message=utils.get_first_error(serializer.errors))

        json_register_response = UserSerializer.register(ktpId=serializer.validated_data['ktpId'], username=serializer.validated_data['username'], loginPassword=serializer.validated_data['loginPassword'],
                                                         phoneNumber=serializer.validated_data['phoneNumber'], birthDate=serializer.validated_data['birthDate'], gender=serializer.validated_data['gender'], email=serializer.validated_data['email']).json()
        if not json_register_response.get('success'):
            return responses.error_response(error_message=json_register_response.get('errMsg'))

        User.objects.create(uid=json_register_response.get('data').get(
            'uid'), pin=serializer.validated_data['pin'], old_password=serializer.validated_data['loginPassword'], current_password=serializer.validated_data['loginPassword'], username=serializer.validated_data['username'], email=serializer.validated_data['email'], gender=serializer.validated_data['gender'])

        create_new_account_response = UserSerializer.create_new_account(
            serializer.validated_data['username'], serializer.validated_data['loginPassword'])
        json_create_new_account_response = create_new_account_response.json()

        if not json_create_new_account_response.get('success'):
            return responses.error_response(error_message=json_create_new_account_response.get('errMsg'))

        response_data = dict(serializer.validated_data)
        response_data['uid'] = json_register_response.get('data').get('uid')
        response_data.pop('loginPassword')

        return responses.success_response(data=response_data)


class __LoginUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(
            username=username, current_password=password).first()

        if not user:
            return responses.error_response(error_message="User not found")

        json_login_response = UserSerializer.login(
            username=username, loginPassword=user.old_password).json()

        if not json_login_response.get('success'):
            return responses.error_response(error_message=json_login_response.get('errMsg'))

        accessToken = json_login_response.get('data').get('accessToken')

        json_get_user_profile_response = UserSerializer.get_user_profile(
            accessToken).json()

        if not json_get_user_profile_response.get('success'):
            return responses.error_response(error_message=json_get_user_profile_response.get('errMsg'))

        json_get_user_profile_response.get('data')['accessToken'] = accessToken
        json_get_user_profile_response.get(
            'data')['is_approved'] = user.is_approved
        json_get_user_profile_response.get(
            'data')['role'] = user.role

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


class __GetUserBankAccountAPIView(APIView):
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


class __CreateTransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        senderAccountNo = request.data.get('senderAccountNo')
        receiverAccountNo = request.data.get('receiverAccountNo')
        amount = request.data.get('amount')
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]
        print(senderAccountNo, receiverAccountNo, amount)

        json_create_transaction_response = UserSerializer.create_transaction(senderAccountNo, receiverAccountNo, amount,
                                                                             access_token).json()

        if not json_create_transaction_response.get('success'):
            return responses.error_response(error_message=json_create_transaction_response.get('errMsg'))

        return responses.success_response(data=json_create_transaction_response.get(
            'data'))


class __GetUserTransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        accountNo = request.data.get('accountNo')
        pageNumber = request.data.get('pageNumber')
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        json_get_transaction_response = UserSerializer.get_transaction(
            accountNo=accountNo, pageNumber=pageNumber, access_token=access_token).json()

        if not json_get_transaction_response.get('success'):
            return responses.error_response(error_message=json_get_transaction_response.get('errMsg'))

        return responses.success_response(data=json_get_transaction_response.get(
            'data'))


class __GetUserTransactionTransferInAPIView(APIView):
    def post(self, request, *args, **kwargs):
        accountNo = request.data.get('accountNo')
        pageNumber = request.data.get('pageNumber')
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        json_get_transaction_response = UserSerializer.get_transaction(
            accountNo=accountNo, pageNumber=pageNumber, access_token=access_token, traxType=["TRANSFER_IN"]).json()

        if not json_get_transaction_response.get('success'):
            return responses.error_response(error_message=json_get_transaction_response.get('errMsg'))

        return responses.success_response(data=json_get_transaction_response.get(
            'data'))


class __GetUserTransactionTransferOutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        accountNo = request.data.get('accountNo')
        pageNumber = request.data.get('pageNumber')
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        json_get_transaction_response = UserSerializer.get_transaction(
            accountNo == accountNo, pageNumber=pageNumber, access_token=access_token, traxType=["TRANSFER_OUT"]).json()

        if not json_get_transaction_response.get('success'):
            return responses.error_response(error_message=json_get_transaction_response.get('errMsg'))

        return responses.success_response(data=json_get_transaction_response.get(
            'data'))


class __ApproveUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_approval_serializer = UserApprovalSerializer(data=request.data)
        user_id = request.data.get('user_id')
        print(user_id)

        user = User.objects.filter(
            uid=user_id).first()

        if not user:
            return responses.error_response(error_message="User not found")

        if not user_approval_serializer.is_valid():
            responses.error_response(
                error_message=utils.get_first_error(user_approval_serializer.errors))
        user_approval_serializer.save()
        user.approve_user(user_approval_serializer.instance)

        return responses.success_response(data={})


class _ChangePasswordUserAPIView(APIView):
    def put(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = User.objects.filter(
            uid=user_id).first()

        if not user:
            return responses.error_response(error_message="User not found")
        
        # new_password = request.data.get('new_password')
        # serializer = UpdatePasswordUserSerializer(user,
        #                                           data=request.data)

        # if not serializer.is_valid():
        #     return Response({"detail":
        #                      utils.get_first_error(serializer.errors)
        #                      }, status=status.HTTP_400_BAD_REQUEST)

        # if (utils.compare_password(serializer.validated_data['password'], user.password)):
        #     return Response({"detail": "New password must be different from the old password"}, status=status.HTTP_400_BAD_REQUEST)
        # serializer.save()
        # ForgotPasswordLink.delete_by_user_id_if_exists(user_id)
        # return Response({"detail": "Password changed."}, status=status.HTTP_200_OK)


create_user_api_view = __CreateUserAPIView.as_view()
login_user_api_view = __LoginUserAPIView.as_view()
get_user_api_view = __GetUserAPIView.as_view()
get_user_bank_account_api_view = __GetUserBankAccountAPIView.as_view()
create_transaction_api_view = __CreateTransactionAPIView.as_view()
get_user_transaction_api_view = __GetUserTransactionAPIView.as_view()
get_user_transaction_transfer_in_api_view = __GetUserTransactionTransferInAPIView.as_view()
get_user_transaction_transfer_out_api_view = __GetUserTransactionTransferOutAPIView.as_view()
approve_user_api_view = __ApproveUserAPIView.as_view()
