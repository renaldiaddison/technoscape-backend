from rest_framework import serializers
from .models import Loan, LoanApproval

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApproval
        exclude = ['is_approved']
    
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ['is_payed']
        