from rest_framework.views import APIView
from .serializers import LoanSerializer, LoanApprovalSerializer
from utils.responses import error_response, success_response
from .models import Loan, LoanApproval
from django.shortcuts import get_object_or_404
import requests
from rest_framework import generics
from utils.permissions import *
from user.serializers import UserSerializer
from utils import utils
from model_api.models import Model
from user.models import User, UserApproval


class _CreateLoanApproval(APIView):
    def post(self, request, *args, **kwargs):

        access_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]

        user_bank_account = UserSerializer.get_user_bank_account(
            access_token).json()['data']['accounts'][0]['accountNo']

        serializer = LoanApprovalSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(error_message=serializer.errors)

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
        return success_response(data=serializer.data)


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
            'message': 'Loan approval has been approved.',
        }

        return success_response(data=response_data)


class _CreateLoanView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoanSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error_message=utils.get_first_error(serializer.errors))

        loan_approval_id = request.data.get('approval')
        loan_approval = get_object_or_404(LoanApproval, pk=loan_approval_id)

        # Get Bearer Token
        bearer_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]
        headers = {'Authorization': f'Bearer {bearer_token}'}

        # Define the response variable with a default value
        response = None

        print(loan_approval.receiverAccountNo)

        response = requests.post("http://34.101.154.14:8175/hackathon/bankAccount/addBalance", json={
            "receiverAccountNo": loan_approval.receiverAccountNo,
            "amount": loan_approval.loan_amount
        }, headers=headers)

        if response.status_code // 100 == 2:
            response_data = response.json()
            serializer.save()
            return success_response(data=response_data)
        else:
            return error_response(error_message=response.text)


class _GetLoan(APIView):
    def get(self, request):
        user_id = self.request.GET.get("user_id")

        loan_approval = LoanApproval.objects.filter(user_id=user_id).last()
        loan = Loan.objects.filter(approval=loan_approval).last()
        print(loan_approval)
        print(loan)
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
            return error_response("Loan approval not found for the user.")
        elif (loan == None):
            return error_response("No unpaid loan found for the user.")


class _PayLoan(APIView):
    def post(self, request, *args, **kwargs):
        loan_id = request.data.get('loan')
        loan = get_object_or_404(Loan, pk=loan_id)
        loan_approval = get_object_or_404(LoanApproval, pk=loan.approval)
        loan.is_payed = True
        loan.save()

        response = None

        # Get Bearer Token
        bearer_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]
        headers = {'Authorization': f'Bearer {bearer_token}'}

        response = requests.post("http://34.101.154.14:8175/hackathon/bankAccount/transaction/create", json={
            "senderAccountNo": loan_approval.receiverAccountNo,
            "receiverAccountNo": "5859456169395245",
            "amount": loan_approval.loan_amount
        }, headers=headers)

        if response.status_code // 100 == 2:
            response_data = response.json()
            return success_response(data="Loan Payed !")
        else:
            return error_response(error_message=response.text)


class _AdminViewApprovals(generics.ListAPIView):
    queryset = LoanApproval.objects.all().order_by('-id')
    serializer_class = LoanApprovalSerializer
    permission_classes = [IsAdmin]


class _AdminViewLoans(generics.ListAPIView):
    queryset = Loan.objects.all().order_by('-id')
    serializer_class = LoanSerializer
    permission_classes = [IsAdmin]


create_loan_approval_view = _CreateLoanApproval.as_view()
approve_loan_approval_view = _ApproveLoanApproval.as_view()
create_loan_view = _CreateLoanView.as_view()
get_loan_view = _GetLoan.as_view()
pay_loan_view = _PayLoan.as_view()
admin_view_approvals = _AdminViewApprovals.as_view()
admin_view_loans = _AdminViewLoans.as_view()
