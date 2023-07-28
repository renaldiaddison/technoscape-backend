# Generated by Django 4.2.3 on 2023-07-28 12:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('married', models.IntegerField()),
                ('dependent', models.IntegerField()),
                ('education', models.IntegerField()),
                ('self_employed', models.IntegerField()),
                ('income', models.BigIntegerField()),
                ('coappliciant_income', models.BigIntegerField()),
                ('property_area', models.IntegerField()),
            ],
            options={
                'db_table': 'user_approvals',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('username', models.TextField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('old_password', models.TextField()),
                ('current_password', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('pin', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d+$', message='Only digits are allowed.')])),
                ('role', models.TextField(default='USER')),
                ('user_approval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userapproval')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
