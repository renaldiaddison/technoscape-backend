# Generated by Django 4.2.3 on 2023-07-29 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_userapproval_credit_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_no',
            field=models.TextField(blank=True, null=True),
        ),
    ]