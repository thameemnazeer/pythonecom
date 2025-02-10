from django.contrib.auth.forms import UserCreationForm
from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=25)
    desc=models.TextField()
    image = models.ImageField(upload_to='image')
    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=25)
    desc=models.TextField()
    image=models.ImageField(upload_to='image')
    price=models.DecimalField(max_digits=15,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product')


    def __str__(self):
        return self.name


