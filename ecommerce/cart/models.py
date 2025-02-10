from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


# Create your models here.
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def subtotal(self):
        return self.product.price*self.quantity
    def __str__(self):
        return self.product.name

class Payment(models.Model):
    name=models.CharField(max_length=30)
    amount=models.IntegerField()
    order_id=models.CharField(max_length=30)
    razorpay_payment_id=models.CharField(max_length=30,blank=True)
    paid=models.BooleanField(default=True)
    def __str__(self):
        return self.order_id


class Order_details(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    address=models.TextField()
    phone=models.IntegerField()
    pin = models.IntegerField()
    order_id=models.CharField(max_length=30)
    payment_status=models.CharField(max_length=30,default='pending')
    delivery_status=models.CharField(max_length=30,default='pending')
    ordered_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.order_id