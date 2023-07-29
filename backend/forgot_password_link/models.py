import uuid
from django.db import models
from user.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone


class ForgotPasswordLink(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "forgot_password_links"

    @classmethod
    def delete_by_user_id_if_exists(cls, user_id):
        forgot_password_link = ForgotPasswordLink.objects.filter(user=user_id)
        forgot_password_link.delete()
