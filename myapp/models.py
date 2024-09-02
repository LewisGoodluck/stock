from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def amount(self):
        return self.quantity * self.price
    
    @property
    def date(self):
        return self.last_updated.ctime()
   
    def __str__(self):
        return self.name
    

class ProductOut(models.Model):
    product_out = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    quantityOut = models.PositiveIntegerField(default=0)
    dateOut = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name