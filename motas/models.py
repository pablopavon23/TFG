from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

# class Builds(models.Model):
#     build_name = models.CharField(max_length=200)
#     user = models.ForeignKey(User)
