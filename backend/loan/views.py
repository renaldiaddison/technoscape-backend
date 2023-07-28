from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoanSerializer, LoanApprovalSerializer
from utils.response import error_response, success_response
from .models import Loan, LoanApproval
from django.shortcuts import get_object_or_404

# Create your views here.

class _CreateLoanApproval(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoanApprovalSerializer(data = request.data)
        if not serializer.is_valid():
            return error_response(error_message=serializer.errors)
        serializer.save()
        return success_response(data = serializer.data)

class _ApproveLoanApproval(APIView):
    # permission_classes = [isAdmin]

    def put(self, request, *args, **kwargs):
        loan_approval_id = request.data.get('loan_approval_id')
        loan_approval = get_object_or_404(LoanApproval, pk=loan_approval_id)
        loan_approval.is_approved = True
        loan_approval.save()

        serializer = LoanApprovalSerializer(loan_approval)
        serialized_data = serializer.data

        return success_response(data=serialized_data)
        
create_loan_approval_view = _CreateLoanApproval.as_view()
approve_loan_approval_view = _ApproveLoanApproval.as_view()

