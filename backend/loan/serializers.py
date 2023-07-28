from rest_framework import serializers
from .models import Loan, LoanApproval
from user.serializers import UserSerializer, ImportantUserDataSerializer
from user.models import User


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
