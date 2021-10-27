from delivery.models import DeliveryBoy
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.db import models
from PIL import Image
# Create your models here.
class Vendor(models.Model):
	STATE_CHOICES = (
		("Andaman & Nicobar Islands",'Andaman & Nicobar Islands'),
		("Andhra Pradesh",'Andhra Pradesh'),
		("Arunachal Pradesh",'Arunachal Pradesh'),
		("Assam",'Assam'),
		("Bihar",'Bihar'),
		("Chandigarh",'Chandigarh'),
		("Chhattisgarh",'Chhattisgarh'),
		("Dadra & Nagar Haveli",'Dadra & Nagar Haveli'),
		("Daman and Diu",'Daman and Diu'),
		("Delhi",'Delhi'),
		("Goa",'Goa'),
		("Gujarat",'Gujarat'),
		("Haryana",'Haryana'),
		("Himachal Pradesh",'Himachal Pradesh'),
		("Jammu & Kashmir",'Jammu & Kashmir'),
		("Jharkhand",'Jharkhand'),
		("Karnataka",'Karnataka'),
		("Kerala",'Kerala'),
		("Lakshadweep",'Lakshadweep'),
		("Madhya Pradesh",'Madhya Pradesh'),
		("Maharashtra",'Maharashtra'),
		("Manipur",'Manipur'),
		("Meghalaya",'Meghalaya'),
		("Mizoram",'Mizoram'),
		("Nagaland",'Nagaland'),
		("Odisha",'Odisha'),
		("Puducherry",'Puducherry'),
		("Punjab",'Punjab'),
		("Rajasthan",'Rajasthan'),
		("Sikkim",'Sikkim'),
		("Tamil Nadu",'Tamil Nadu'),
		("Telangana",'Telangana'),
		("Tripura",'Tripura'),
		("Uttarakhand",'Uttarakhand'),
		("Uttar Pradesh",'Uttar Pradesh'),
		("West Bengal",'West Bengal'),
		)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)	
	user = models.OneToOneField(User, related_name='vendor'  ,on_delete=models.CASCADE,primary_key=True)
	email = models.EmailField()
	badge=models.CharField(max_length=150, blank=True, null=True)
	photo = models.ImageField(default='user.png',upload_to='user_photos/')
	mobile = models.CharField(max_length=10,null=True)
	gst_Number = models.CharField(max_length=15,null=True)
	shop_Name = models.CharField(max_length=500,null=True)
	alternate_mobile = models.CharField(max_length=10,null=True,blank=True)
	shop_Address = models.TextField()
	pincode = models.CharField(max_length=6, null=True)
	landmark = models.CharField(max_length=500, null=True, blank=True)
	locality = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
	account_Holder_Name = models.CharField(max_length=50, null=True)
	account_Number = models.CharField(max_length=20, null=True)
	ifsc_Code = models.CharField(max_length=11, null=True)

	def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img = Image.open(self.photo.path)
	    if img.height > 300 or img.width > 300:
		    output_size = (300, 300)
		    img.thumbnail(output_size)
		    img.save(self.photo.path)

	def image_tag(self):
		return mark_safe('<img src="%s" width="50" height="50" />' % (self.photo.url))



	class Meta:
		ordering = ['first_name']

	def __str__(self):
		return self.gst_Number



