from django.db import models


class User(models.Model):
    pin = models.CharField(max_length=6)
