from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ForgotPasswordLink
from .serializers import ForgotPasswordLinkSerializer
from utils import utils, responses
from user.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone


class __GenerateForgotPasswordLinkAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        user = User.objects.filter(
            email=email).first()

        if not user:
            return responses.error_response(error_message="User not found")

        ForgotPasswordLink.delete_by_user_id_if_exists(user.uid)

        forgot_password_link_serializer = ForgotPasswordLinkSerializer(
            data={'user': user.uid})
        if not forgot_password_link_serializer.is_valid():
            return responses.error_response(error_message=utils.get_first_error(
                forgot_password_link_serializer.errors))
        forgot_password_link_serializer.save()

        utils.send_user_forgot_password_email(
            to=user.email, forgot_password_link_param="/"+forgot_password_link_serializer.data['id'])

        return responses.success_response(data={})


class __ValidateForgotPasswordLinkAPIView(APIView):
    def post(self, request, *args, **kwargs):
        forgot_password_link_id = request.data.get('forgot_password_link_id')

        forgot_password_link = ForgotPasswordLink.objects.filter(
            pk=forgot_password_link_id).first()

        if not forgot_password_link:
            return responses.error_response(error_message="Link not valid")

        if timezone.now() > forgot_password_link.created_at + utils.get_expiration_duration():
            forgot_password_link.delete()
            return responses.error_response(error_message="Forgot password link expired")

        return responses.success_response(data={})


generate_forgot_password_link_api_view = __GenerateForgotPasswordLinkAPIView.as_view()
validate_forgot_password_link_api_view = __ValidateForgotPasswordLinkAPIView.as_view()
