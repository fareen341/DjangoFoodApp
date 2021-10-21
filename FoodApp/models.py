from django.db import models
from django.contrib.auth.models import User, Group
import datetime



# Create your models here.
class Food(models.Model):
    category1=[('veg','vegetarian'),
                ('non-veg','non-vegetarian')]
    name=models.CharField(max_length=25)
    price=models.FloatField()
    quantity=models.IntegerField()
    type=models.CharField(max_length=25)
    category=models.CharField(choices=category1, default='veg', max_length=40)
    image=models.ImageField(upload_to='meida/')

    # class Meta:
    #     db_table="Fooddb"        #provide new name to the table

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    contact = models.CharField(max_length=10)
    class Meta:
        db_table = 'UserProfiledb'

admin,status=Group.objects.get_or_create(name='admin')
customer,status=Group.objects.get_or_create(name='customer')

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    foodobj = models.ForeignKey(Food, on_delete=models.CASCADE)
    qnt = models.IntegerField(default=1)
    price = models.FloatField()
    class Meta:
        db_table = 'Cart'

    
class OrderSummary(models.Model):
    date1=datetime.datetime.now().strftime(' %Y-%m-%d %h:%m ')
    date=models.CharField(default=str(date1), max_length=10)
    totalamount=models.FloatField()
    status=models.CharField(max_length=20, default='pending',choices=[('pending','pending'),('delivered','delivered')])
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table='OrderSummary'

class Orders(models.Model):
    ordersobj=models.ForeignKey(OrderSummary, on_delete=models.CASCADE)
    foodobj=models.ForeignKey(Food, on_delete=models.CASCADE)
    totalprice=models.FloatField()
    quantity=models.IntegerField()
    class Meta:
        db_table='Orders' 