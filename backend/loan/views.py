from rest_framework.views import APIView
from .serializers import LoanSerializer, LoanApprovalSerializer, LoanWithLoanApprovalSerializer, LoanApprovalWithUserSerializer
from utils.responses import error_response, success_response
from .models import Loan, LoanApproval
from django.shortcuts import get_object_or_404
import requests
from rest_framework import generics
from utils.permissions import *
from user.serializers import UserSerializer
from utils import utils, responses
from model_api.models import Model
from user.models import User, UserApproval
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class _CreateLoanApproval(APIView):
    def post(self, request, *args, **kwargs):

        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        response = UserSerializer.get_user_bank_account(
            access_token)

        if response.status_code == 401:
            return responses.error_response(error_message="Unauthorized", status=401)

        user_bank_account = response.json()['data']['accounts'][0]['accountNo']

        serializer = LoanApprovalSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(error_message=utils.get_first_error(serializer.errors))

        # Rate total 5%, 6%, 7%
        if (serializer.validated_data['loan_days_term'] == 360):
            serializer.validated_data['rate'] = 7
        elif (serializer.validated_data['loan_days_term'] == 270):
            serializer.validated_data['rate'] = 6

        # model predict
        user_id = request.data.get('user')
        user = get_object_or_404(User, uid=user_id)
        user_approval: UserApproval = user.user_approval
        model_instance = Model.get_instance()
        # 	Gender, Married, Dependent, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area
        prediction = model_instance.predict(
            [[user.gender, user_approval.married, user_approval.dependent, user_approval.education, user_approval.self_employed, user_approval.income, user_approval.coappliciant_income, serializer.validated_data['loan_amount'], serializer.validated_data['loan_days_term'], user_approval.credit_history, user_approval.property_area]])
        if prediction[0] == 0:
            return success_response(data={
                "prediction": prediction[0]
            })

        serializer.validated_data['receiverAccountNo'] = user_bank_account
        serializer.save()
        utils.send_loan_invitation_email(user.email)
        return success_response(data={
            "prediction": prediction[0]
        })


class _ApproveLoanApproval(APIView):
    permission_classes = [IsAdmin]

    def put(self, request, *args, **kwargs):
        loan_approval_id = request.data.get('loan_approval_id')
        loan_approval = get_object_or_404(LoanApproval, pk=loan_approval_id)

        loan_approval.is_approved = True
        loan_approval.save()

        serializer = LoanApprovalSerializer(loan_approval)
        serialized_data = serializer.data

        response_data = {
            'loan_approval': serialized_data,
            'message': 'Loan approval has been approved and moved to history.',
        }

        return success_response(data=response_data)


class _UnapproveLoanApproval(APIView):
    permission_classes = [IsAdmin]

    def put(self, request, *args, **kwargs):
        loan_approval_id = request.data.get('loan_approval_id')
        loan_approval = get_object_or_404(LoanApproval, pk=loan_approval_id)

        loan_approval.is_approved = False
        loan_approval.save()

        serializer = LoanApprovalSerializer(loan_approval)
        serialized_data = serializer.data

        response_data = {
            'loan_approval': serialized_data,
            'message': 'Loan approval has been declined and moved to history.',
        }

        return success_response(data=response_data)


class _CreateLoanView(APIView):
    def post(self, request, *args, **kwargs):
        loan_approval_id = request.data.get('approval')
        loan = Loan.objects.filter(approval_id=loan_approval_id).first()

        if loan:
            return error_response(error_message="Loan already claimed")

        loan_approval = get_object_or_404(LoanApproval, pk=loan_approval_id)

        # Get Bearer Token
        bearer_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]
        headers = {'Authorization': f'Bearer {bearer_token}'}

        # Define the response variable with a default value
        response = None

        serializer = LoanSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error_message=utils.get_first_error(serializer.errors))

        response = requests.post("http://34.101.154.14:8175/hackathon/bankAccount/addBalance", json={
            "receiverAccountNo": loan_approval.receiverAccountNo,
            "amount": loan_approval.loan_amount
        }, headers=headers)
        response_data = response.json()
        if response_data.get('success'):
            serializer.save()
            return success_response(data=response_data)
        else:
            return error_response(error_message=response.text)


class _GetLoan(APIView):
    def get(self, request):
        user_id = self.request.GET.get("user_id")

        loan_approval = LoanApproval.objects.filter(user_id=user_id).last()
        loan = Loan.objects.filter(approval=loan_approval).last()
        loan_approval_serializer = LoanApprovalSerializer(loan_approval)
        loan_serializer = LoanSerializer(loan)

        response_data = {
            "loan_approval": loan_approval_serializer.data,
            "loan": None if loan is None else loan_serializer.data
        }

        if (loan != None):
            return success_response(data=response_data)
        elif (loan == None and loan_approval):
            return success_response(data=response_data)
        elif (loan_approval == None):
            return success_response(data={})
        elif (loan == None):
            return success_response(data={})


class _PayLoan(APIView):
    def post(self, request, *args, **kwargs):
        loan_id = request.data.get('loan')
        loan = get_object_or_404(Loan, pk=loan_id)
        loan.is_payed = True
        loan.approval.is_done = True
        loan.save()
        loan.approval.save()

        response = None

        # Get Bearer Token
        bearer_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]
        headers = {'Authorization': f'Bearer {bearer_token}'}

        months_difference = relativedelta(
            timezone.now(), loan.created_at).months

        excess_amount = (months_difference * 1) / 100

        response = requests.post("http://34.101.154.14:8175/hackathon/bankAccount/transaction/create", json={
            "senderAccountNo": loan.approval.receiverAccountNo,
            "receiverAccountNo": "5859455512376902",
            "amount": loan.approval.loan_amount + (loan.approval.rate * loan.approval.loan_amount / 100) + excess_amount
        }, headers=headers)

        if response.status_code == 401:
            return error_response(error_message="Unauthorized", status=401)

        response_data = response.json()
        if (response_data.success == False):
            return error_response(error_message=response_data.get('errMsg'))

        return success_response(data=response_data)


class _GetLoanHistory(generics.ListAPIView):
    serializer_class = LoanWithLoanApprovalSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        user = get_object_or_404(User, uid=user_id)
        if (user.role == 'ADMIN'):
            return Loan.objects.filter(approval__is_done=True).order_by('-created_at')
        else:
            return Loan.objects.filter(approval__is_done=True, approval__user=user_id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        print(self.get_queryset())
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


class _AdminViewLoans(generics.ListAPIView):
    queryset = Loan.objects.all().order_by('-id')
    serializer_class = LoanSerializer


class _GetAllApproval(generics.ListAPIView):
    queryset = LoanApproval.objects.all().order_by('-created_at')
    serializer_class = LoanApprovalWithUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


# class _GetLoanHistory(generics.ListAPIView):
#     serializer_class = LoanSerializer

#     def get_queryset(self):
#         user_id = self.request.query_params.get('user_id')
#         if user_id:
#             return LoanHistory.objects.filter(approval__user_id=user_id)
#         else:
#             return list()


# class _GetLoanApprovalHistory(generics.ListAPIView):
#     serializer_class = LoanApprovalSerializer

#     def get_queryset(self):
#         user_id = self.request.query_params.get('user_id')
#         if user_id:
#             return LoanApprovalHistory.objects.filter(user_id=user_id)
#         else:
#             return list()


create_loan_approval_view = _CreateLoanApproval.as_view()
approve_loan_approval_view = _ApproveLoanApproval.as_view()
unapprove_loan_approval_view = _UnapproveLoanApproval.as_view()
create_loan_view = _CreateLoanView.as_view()
get_loan_view = _GetLoan.as_view()
pay_loan_view = _PayLoan.as_view()
# admin_view_approvals = _AdminViewApprovals.as_view()
get_loan_history_view = _GetLoanHistory.as_view()
admin_view_loans = _AdminViewLoans.as_view()
get_all_approval_view = _GetAllApproval.as_view()
