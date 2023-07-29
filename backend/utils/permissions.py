from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from user.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        if user.role == "ADMIN":
            return True
        return False
