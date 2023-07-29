from rest_framework import serializers
from .models import Loan, LoanApproval
from user.serializers import UserSerializer, ImportantUserDataSerializer
from user.models import User


class LoanApprovalSerializer(serializers.ModelSerializer):
    receiverAccountNo = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = LoanApproval
        fields = '__all__'
        read_only_fields = ['receiverAccountNo', 'is_done']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

# Custom Serializers

class LoanApprovalWithUserSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = LoanApproval
        fields = ['id', 'user', 'loan_amount', 'loan_days_term',
                  'receiverAccountNo', 'is_approved', 'created_at', 'user_data']

    def get_user_data(self, obj):
        serializer = ImportantUserDataSerializer(obj.user)
        return serializer.data

class LoanWithLoanApprovalSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()
    loan_approval_data = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'approval', 'is_payed', 'created_at', 'user_data', 'loan_approval_data']

    def get_user_data(self, obj):
        serializer = ImportantUserDataSerializer(obj.approval.user)
        return serializer.data

    def get_loan_approval_data(self, obj):
        serializer = LoanApprovalSerializer(obj.approval)
        return serializer.data