from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
    uid = models.BigAutoField(primary_key=True,
                              editable=False)
    pin = models.CharField(max_length=6, validators=[RegexValidator(
        r'^\d+$', message='Only digits are allowed.')],)
    role = models.TextField(default="USER")

    class Meta:
        db_table = "users"
