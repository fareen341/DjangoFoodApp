from django.contrib import admin
from django.urls import path
from FoodApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('addfood/',views.AddFood, name='addfood'),
    path('menu/',views.showFood, name="menu"),
    path('update/<int:id>',views.updateFoods),
    path('delete/<int:id>',views.deleteFood),  
    path('register/', views.addUser, name="register"),
    path('login/',views.loginuser, name="login"),
    path('customer/',views.showUser, name="customer"),
    path('logout/',views.logoutuser, name="logout"),
    path('index/',views.index, name="index"),
    path('customerlist/', views.showUserProfile, name="customerlist"),
    path('profile/',views.showUserProfile, name="profile"),
    path('editprofile/',views.editUserProfile, name="editprofile"),
    path('addtocart/',views.addtocart, name="addtocart"),
    path('mycart/',views.showcart, name="mycart"),
    path('updatecart/',views.updateCart, name="updatecart"),
    path('deletecart/<int:id>',views.deleteCart, name="deletecart"),
    path('placeorder/',views.addOrders, name="placeorder"),
    path('showorders/',views.showorders, name="showorders"),
    # path('payment/',views.paymentView, name="payment")



]

if settings.DEBUG:		
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
