from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils import utils, responses
from .models import User
from .serializers import UserSerializer, UserApprovalSerializer, UpdatePasswordUserSerializer
from forgot_password_link.models import ForgotPasswordLink


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

        response = UserSerializer.get_user_profile(
            accessToken)

        if response.status_code == 401:
            responses.error_response(error_message="Unauthorized", status=401)

        json_get_user_profile_response = response.json()

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

        response = UserSerializer.get_user_profile(
            access_token)

        if response.status_code == 401:
            return responses.error_response(error_message="Unauthorized", status=401)

        json_get_user_profile_response = response.json()

        if not json_get_user_profile_response.get('success'):
            return responses.error_response(error_message=json_get_user_profile_response.get('errMsg'))

        return responses.success_response(data=json_get_user_profile_response.get('data'))


class __GetUserBankAccountAPIView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        response = UserSerializer.get_user_bank_account(
            access_token=access_token)

        if response.status_code == 401:
            return responses.error_response(error_message="Unauthorized", status=401)

        json_get_user_bank_account_response = response.json()

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

        response = UserSerializer.create_transaction(senderAccountNo, receiverAccountNo, amount,
                                                     access_token)

        if response.status_code == 401:
            return responses.error_response(error_message="Unauthorized", status=401)

        json_create_transaction_response = response.json()

        if not json_create_transaction_response.get('success'):
            return responses.error_response(error_message=json_create_transaction_response.get('errMsg'))

        return responses.success_response(data=json_create_transaction_response.get(
            'data'))


class __GetUserTransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        accountNo = request.data.get('accountNo')
        pageNumber = request.data.get('pageNumber')
        transactionType = request.data.get('transactionType')

        traxType = []

        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        if transactionType is None:
            traxType = ["TRANSFER_IN", "TRANSFER_OUT"]

        traxType.append(transactionType)

        response = UserSerializer.get_transaction(
            accountNo=accountNo, pageNumber=pageNumber, access_token=access_token)

        if response.status_code == 401:
            return responses.error_response(error_message="Unauthorized", status=401)

        json_get_transaction_response = response.json()

        if not json_get_transaction_response.get('success'):
            return responses.error_response(error_message=json_get_transaction_response.get('errMsg'))

        data = json_get_transaction_response.get(
            'data')

        transactions = data.get('transactions')

        for transaction in transactions:
            print(transaction)
            sender_account_info_response = UserSerializer.get_bank_account_info(
                access_token=access_token, accountNo=transaction.get('senderAccountNo'))

            receiver_account_info_response = UserSerializer.get_bank_account_info(
                access_token=access_token, accountNo=transaction.get('receiverAccountNo'))

            if sender_account_info_response.status_code == 401 or receiver_account_info_response.status_code == 401:
                return responses.error_response(error_message="Unauthorized", status=401)

            transaction['senderAccountInfo'] = sender_account_info_response.json().get(
                'data')
            transaction['receiverAccountInfo'] = receiver_account_info_response.json().get(
                'data')

            transaction['traxType'] = utils.translate_en_to_id(
                transaction['traxType'])

        return responses.success_response(data=data)


class __GetUserTransactionTransferInAPIView(APIView):
    def post(self, request, *args, **kwargs):
        accountNo = request.data.get('accountNo')
        pageNumber = request.data.get('pageNumber')
        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        response = UserSerializer.get_transaction(
            accountNo=accountNo, pageNumber=pageNumber, access_token=access_token, traxType=["TRANSFER_IN"])

        if response.status_code == 401:
            return responses.error_response(error_message="Unauthorized", status=401)

        json_get_transaction_response = response.json()

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

        response = UserSerializer.get_transaction(
            accountNo=accountNo, pageNumber=pageNumber, access_token=access_token, traxType=["TRANSFER_OUT"])

        if response.status_code == 401:
            return responses.error_response(error_message="Unauthorized", status=401)

        json_get_transaction_response = response.json()

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


class __VerifyPINAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        pin = request.data.get('pin')

        user = User.objects.filter(
            uid=user_id).first()

        if not user:
            return responses.error_response(error_message="User not found")

        if pin != user.pin:
            return responses.error_response(error_message="PIN Incorrect")

        return responses.success_response(data={})


class _ForgotPasswordUserAPIView(APIView):
    def put(self, request, *args, **kwargs):
        forgot_password_link_id = request.data.get('forgot_password_link_id')

        forgot_password_link = ForgotPasswordLink.objects.filter(
            pk=forgot_password_link_id).first()

        if not forgot_password_link:
            return responses.error_response(error_message="Link not valid")

        user = User.objects.filter(
            uid=forgot_password_link.user.uid).first()

        if not user:
            return responses.error_response(error_message="User not found")

        serializer = UpdatePasswordUserSerializer(user,
                                                  data=request.data)

        if not serializer.is_valid():
            return responses.error_response(error_message=utils.get_first_error(serializer.error))

        if serializer.validated_data['current_password'] == user.current_password:
            return responses.error_response(error_message="New password must be different from the old password")

        serializer.save()
        forgot_password_link.delete()
        return responses.success_response(data={})


create_user_api_view = __CreateUserAPIView.as_view()
login_user_api_view = __LoginUserAPIView.as_view()
get_user_api_view = __GetUserAPIView.as_view()
get_user_bank_account_api_view = __GetUserBankAccountAPIView.as_view()
create_transaction_api_view = __CreateTransactionAPIView.as_view()
get_user_transaction_api_view = __GetUserTransactionAPIView.as_view()
get_user_transaction_transfer_in_api_view = __GetUserTransactionTransferInAPIView.as_view()
get_user_transaction_transfer_out_api_view = __GetUserTransactionTransferOutAPIView.as_view()
approve_user_api_view = __ApproveUserAPIView.as_view()
forgot_password_api_view = _ForgotPasswordUserAPIView.as_view()
verify_pin_api_view = __VerifyPINAPIView.as_view()
