from django.db import models
import uuid
from user.models import User
from django.utils.timezone import now

class LoanApproval(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    loan_amount = models.IntegerField()
    loan_days_term = models.IntegerField()
    receiverAccountNo = models.TextField()
    is_approved = models.BooleanField(null=True)
    rate = models.IntegerField(default=5)
    created_at = models.DateTimeField(default=now)
    is_done = models.BooleanField(null=False)
    
    class Meta:
        db_table = "loan_approvals"

class Loan(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    approval = models.ForeignKey(LoanApproval, on_delete = models.CASCADE, null=True)
    is_payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "loans"
        

    