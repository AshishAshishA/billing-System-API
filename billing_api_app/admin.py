from django.contrib import admin
from .models import Customer, Product, BillItem, Bill

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(BillItem)
admin.site.register(Bill)