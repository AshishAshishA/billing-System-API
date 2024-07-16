from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField(max_length=70,blank=True)
    total_shopping = models.FloatField(default = 0)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 250)
    price = models.FloatField()


class Bill(models.Model):
    customer = models.ForeignKey(Customer, related_name='bill', on_delete=models.SET_NULL, blank=True, null=True)
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class BillItem(models.Model):                           # act as a single product with multiple quantity
    bill = models.ForeignKey(Bill, related_name='billItems', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField()
