from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import fields
from .models import ProductReview, UserAddressBook, UserDetail, CartOrderItems

class RecivedForm(forms.ModelForm):
	class Meta:
		model = CartOrderItems
		fields=('order_status',)

class SignupForm(UserCreationForm):
	class Meta:
		model=User
		fields=('first_name','last_name','username','email','password1','password2')

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')

# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=(           
			'first_name',
		   'last_name',
            'email',
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
			'status')

# ProfileEdit
class UserDetailForm(forms.ModelForm):
	class Meta:
		model=UserDetail
		fields = [
			'first_name','last_name','email',
			'dob',
			'photo',
			'mobile',
			
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
			'Gender',
		]



