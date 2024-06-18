from django.db import models
from payments.models import Transaction
from process_occ.models import Order
from datetime import datetime



class Shipping(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE ,null=True, blank=True)

    tracking_no = models.CharField(max_length=25, null=True, blank=True, unique=True)
    services = models.CharField(max_length=20, null=True, blank=True)
    weight =  models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(null=True, blank= True)
    
    STATUS_CHOICES =[
        ("processing","Processing"),
        ("on_the_way", "On The Way"),
        ("arrived" , "Arrived")
    ] 
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, null=True, blank=True)

    tracking = models.JSONField(max_length=600, null=True, blank=True)


    def __str__(self):
        return f"Tracking No # {self.tracking_no}"
    
    def save(self,  *args, **kwargs):
        current_timestamp = datetime.now().timestamp()

        self.tracking_no = current_timestamp

        super().save(*args, **kwargs)


class CarbonOffset(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,null=True ,blank=True)
    offSet_price = models.FloatField(null=True, blank=True)
    offSet_status = models.CharField(max_length=30, null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"CarbonOffset for Order {self.order.id}"

