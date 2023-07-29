from rest_framework import serializers
from .models import ForgotPasswordLink


class ForgotPasswordLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgotPasswordLink
        fields = '__all__'
