from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoanSerializer, LoanApprovalSerializer
from utils.responses import error_response, success_response
from .models import Loan, LoanApproval
from django.shortcuts import get_object_or_404
import requests


class _CreateLoanApproval(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoanApprovalSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(error_message=serializer.errors)
        serializer.save()
        return success_response(data=serializer.data)


class _ApproveLoanApproval(APIView):
    # permission_classes = [isAdmin]

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
            return error_response(error_message=serializer.errors)

        loan_approval_id = request.data.get('approval')
        loan_approval = get_object_or_404(LoanApproval, pk=loan_approval_id)

        

        # Get Bearer Token
        bearer_token = request.META.get(
            'HTTP_AUTHORIZATION', '').split('Bearer ')[1]
        headers = {'Authorization': f'Bearer {bearer_token}'}

        # Define the response variable with a default value
        response = None

        response = requests.post("http://34.101.154.14:8175/hackathon/bankAccount/addBalance", json={
            "receiverAccountNo": loan_approval.receiverAccountNo,
            "amount": loan_approval.loan_amount
        }, headers=headers, timeout=12)

        if response.status_code // 100 == 2:
            response_data = response.json()
            serializer.save()
            return success_response(data=response_data)
        else:
            return error_response(error_message=response.text)
        
class _GetLoan(APIView):
    def get(self, request):
        user_id = self.request.GET.get("user_id")

        try:
            loan_approval = LoanApproval.objects.get(user_id=user_id, is_approved=True)
            loan = Loan.objects.get(approval=loan_approval, is_payed=False)
            serializer = LoanSerializer(loan)
            return success_response(serializer.data)
        except LoanApproval.DoesNotExist:
            return error_response("Loan approval not found for the user.")
        except Loan.DoesNotExist:
            return error_response("No unpaid loan found for the user.")
        
create_loan_approval_view = _CreateLoanApproval.as_view()
approve_loan_approval_view = _ApproveLoanApproval.as_view()
create_loan_view = _CreateLoanView.as_view()

