from rest_framework import serializers
from .models import Loan, LoanApproval


class LoanApprovalSerializer(serializers.ModelSerializer):
    receiverAccountNo = serializers.CharField(allow_null=True, required=False)
    
    class Meta:
        model = LoanApproval
        fields = '__all__' 
        read_only_fields = ['receiverAccountNo']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'      
