from django.db import models
import uuid
from user.models import User

# Create your models here.
class LoanApproval(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # user = models.ForeignKey(User, on_delete = models.CASCADE)
    loan_amount = models.IntegerField()
    loan_days_term = models.IntegerField()
    receiverAccountNo = models.TextField()
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        db_table = "loan_approvals"

class Loan(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    approval = models.ForeignKey(LoanApproval, on_delete = models.CASCADE, null=True)
    is_payed = models.BooleanField(default=False)

    class Meta:
        db_table = "loans"
        




    