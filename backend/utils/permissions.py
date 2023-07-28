from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_id = request.data.get('user_id')
        user = get_object_or_404(pk=user_id)
        if user.role == "ADMIN":
            return True
        return False
