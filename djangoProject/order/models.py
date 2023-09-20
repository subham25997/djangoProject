from django.db import models


class Order(models.Model):
    order_no = models.BigIntegerField(primary_key=True)
    customer_id = models.BigIntegerField()
    product_id = models.BigIntegerField()
    created_by_id = models.BigIntegerField()
    customer_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    product_qty = models.BigIntegerField()
    contact_person = models.CharField(max_length=250)
    created_by = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    order_date = models.DateTimeField()
