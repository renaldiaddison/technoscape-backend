from django.db import models
from django.core.validators import RegexValidator


class UserApproval(models.Model):
    married = models.IntegerField()
    dependent = models.IntegerField()
    education = models.IntegerField()
    self_employed = models.IntegerField()
    income = models.BigIntegerField()
    coappliciant_income = models.BigIntegerField()
    property_area = models.IntegerField()
    credit_history = models.IntegerField()

    class Meta:
        db_table = "user_approvals"


class User(models.Model):
    uid = models.BigAutoField(primary_key=True,
                              editable=False)
    username = models.TextField(unique=True)
    email = models.EmailField(unique=True)
    gender = models.IntegerField(default=0)
    old_password = models.TextField()
    current_password = models.TextField()
    user_approval = models.ForeignKey(
        UserApproval, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    pin = models.CharField(max_length=6, validators=[RegexValidator(
        r'^\d+$', message='Only digits are allowed.')],)
    role = models.TextField(default="USER")
    account_no = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "users"

    def approve_user(self, user_approval_instance):
        self.is_approved = True
        self.user_approval = user_approval_instance
        self.save()
