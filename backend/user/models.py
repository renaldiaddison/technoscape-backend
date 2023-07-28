from django.db import models


class User(models.Model):
    pin = models.CharField(max_length=6)


class UserRole(models.Model):
    roleName = models.TextField()
