from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=255, null=False)


