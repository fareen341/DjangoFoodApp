from django import forms
from django.db import models
from .models import Food, UserProfile
from django.contrib.auth.models import User

class FoodForm(forms.ModelForm):
    category1=[('veg','vegetarian'),
                ('non-veg','non-vegetarian')]
    category=forms.ChoiceField(choices=category1) 
    image=forms.ImageField()           
    class Meta:
        model=Food
        fields='__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','first_name','last_name','password','email']

class UserProfileForm(forms.ModelForm):
    role1=[('customer','customer'),('admin','admin')]
    role=forms.ChoiceField(widget=forms.RadioSelect(),choices=role1)
    class Meta:
        model = UserProfile
        fields=['location','contact']