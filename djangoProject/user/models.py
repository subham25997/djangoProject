from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
