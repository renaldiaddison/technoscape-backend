# Generated by Django 4.2.3 on 2023-07-28 14:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApproval',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('loan_amount', models.IntegerField()),
                ('loan_days_term', models.IntegerField()),
                ('receiverAccountNo', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'loan_approvals',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_payed', models.BooleanField(default=False)),
                ('approval', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.loanapproval')),
            ],
            options={
                'db_table': 'loans',
            },
        ),
    ]
