from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import Vendor
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from product.models import Product
from main.models import CartOrder, CartOrderItems


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category','title', 'details', 'specs', 'brand','image1','image2','image3','image4','image5', 'size','color',  'quantity','price_not', 'price','discount', 'status']

class VendorProfileForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['first_name','last_name', 'mobile', 'badge','email', 'mobile', 'alternate_mobile', 'photo', 'gst_Number', 'shop_Name', 'shop_Address', 'pincode', 'landmark', 'locality', 'city', 'state', 'account_Holder_Name', 'account_Number', 'ifsc_Code']
           

class VendorSignUpForm(UserCreationForm):
	
	first_name = forms.CharField(widget=forms.TextInput(attrs={}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={}))
	username = forms.CharField(label=("Mobile Number/Email"),widget=forms.TextInput(attrs={'oninput':'validate()'}))
	gst = forms.CharField(label=("GST Number"),widget=forms.TextInput(attrs={}))
	shop = forms.CharField(label=("Company/Shop Name"),widget=forms.TextInput(attrs={}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	password2  = forms.CharField(label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2','gst', 'shop']


class CartOrderItemForm(ModelForm):
	class Meta:
		model = CartOrderItems
		fields = ['order_status', 'deliveryboy']

class CartOrderForm(ModelForm):
	class Meta:
		model = CartOrder
		fields = ['order_status', 'deliveryboy']