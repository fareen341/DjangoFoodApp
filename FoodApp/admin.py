from django.contrib import admin
from .models import Food, OrderSummary, Orders, UserProfile, Cart


# Register your models here.
class FoodAdmin(admin.ModelAdmin):
	list_display=['name','price','quantity','type','category','image']
admin.site.register(Food, FoodAdmin)
admin.site.register(UserProfile)


class CartAdmin(admin.ModelAdmin):
	list_display = ['customer','foodobj','qnt','price']
admin.site.register(Cart, CartAdmin)


admin.site.register(OrderSummary)
admin.site.register(Orders)