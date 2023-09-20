from django.db import models


class Menus(models.Model):
    menu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    roles = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

