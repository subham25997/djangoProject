from django.db import models


class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    contact_person = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=50)
