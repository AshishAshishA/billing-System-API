from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Customer, Product, Bill, BillItem


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user_name = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create(username=user_name, password=password)

        user.set_password(password)
        user.save()

        return user



class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price']

class billItemSerializer(serializers.ModelSerializer):
    product = productSerializer()
    class Meta:
        model = BillItem
        fields = ['product','quantity']

class billSerializer(serializers.ModelSerializer):
    customer = customerSerializer()
    billItems = billItemSerializer(many=True)
    class Meta:
        model = Bill
        fields = ['customer','billItems','total_amount','payment_method','date_created','date_updated']
        read_only_fields = ['total_amount','date_created','date_updated']

    def create(self, validated_data):
        print(validated_data)
        customer_data = validated_data.pop('customer')
        billItems_data = validated_data.pop('billItems')

        customer = None

        print(customer_data.get('email'))

        try:
            customer = Customer.objects.get(email=customer_data.get('email'))

        except:
            customer = Customer.objects.create(**customer_data)
            print('new customer created')
            

        total_amount = 0
        bill = Bill.objects.create(customer=customer, total_amount=total_amount, **validated_data)

        
        for bill_item_data in billItems_data:
            product_data = bill_item_data.pop('product')
            product = Product.objects.create(**product_data)
            bill_item = BillItem.objects.create(bill=bill, product=product, **bill_item_data)
            total_amount += (product.price)*(bill_item.quantity)

        customer.total_shopping += total_amount
        bill.total_amount = total_amount

        customer.save()
        bill.save()

        return bill

    def update(self, instance, validated_data):

        customer_data = validated_data.get('customer', None)
        instance.payment_method = validated_data.pop('payment_method')
        bill_items_data = validated_data.pop('billItems')
        customer = instance.customer

        if 'name' in customer_data.keys():
            customer.name = customer_data.get('name')
        if 'email' in customer_data.keys():
            customer.email = customer_data.get('email')

        total_amount = 0

        instance.billItems.all().delete()
        for item in bill_items_data:
            product_data = item.pop('product')
            product = Product.objects.create(**product_data)
            print(item)
            print(product.name)
            bill_item = BillItem.objects.create(bill=instance, product=product, **item)

            total_amount += (product.price)*(bill_item.quantity)

        customer.total_shopping += (total_amount - instance.total_amount)
        instance.total_amount = total_amount

        customer.save()
        instance.save()

        return instance


class billSummarySerializer(serializers.ModelSerializer):
    billItems = billItemSerializer(many = True)
    class Meta:
        model = Bill
        fields = ['total_amount','payment_method','billItems']

class customerWithBillSerializer(serializers.ModelSerializer):
    bill = billSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['name','email','total_shopping','bill']
        

        

        