from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from product.models import Product
from PIL import Image
from vendor.models import Vendor
from delivery.models import DeliveryBoy
# Create your models here.

paymentstatus_choice = (
    ('cashondelivery', 'Cash On Delivery'),
    ('paid', 'Paid'),
)
# Order
status_choice = (
    ('process', 'In Process'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        choices=status_choice, default='process', max_length=150)
    vendor = models.ForeignKey(
        Vendor, related_name='userorder', on_delete=models.CASCADE, blank=True, null=True)
    deliveryboy = models.ForeignKey(
        DeliveryBoy, related_name='userorder', on_delete=models.CASCADE, blank=True, null=True)
    payment = models.CharField(
        choices=paymentstatus_choice, max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = '1. Orders'

# OrderItems


class CartOrderItems(models.Model):
    user = models.ForeignKey(User, related_name='orderitem',
                             on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(
        CartOrder, related_name='orderitem', on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, related_name='orderitem', on_delete=models.CASCADE, blank=True, null=True)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    color = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=200, blank=True, null=True)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        choices=status_choice, default='process', max_length=150)
    deliveryboy = models.ForeignKey(
        DeliveryBoy, related_name='orderitem', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = '2. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:25px; background-color:%s;"></div>' % (self.color))


# Product Review
RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.CharField(choices=RATING, max_length=150)

    class Meta:
        verbose_name_plural = '3. Reviews'

    def get_review_rating(self):
        return self.review_rating

# WishList


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '4. Wishlist'


# AddressBook
class OrderAddressBook(models.Model):
    STATE_CHOICES = (
        ("Andaman & Nicobar Islands", 'Andaman & Nicobar Islands'),
        ("Andhra Pradesh", 'Andhra Pradesh'),
        ("Arunachal Pradesh", 'Arunachal Pradesh'),
        ("Assam", 'Assam'),
        ("Bihar", 'Bihar'),
        ("Chandigarh", 'Chandigarh'),
        ("Chhattisgarh", 'Chhattisgarh'),
        ("Dadra & Nagar Haveli", 'Dadra & Nagar Haveli'),
        ("Daman and Diu", 'Daman and Diu'),
        ("Delhi", 'Delhi'),
        ("Goa", 'Goa'),
        ("Gujarat", 'Gujarat'),
        ("Haryana", 'Haryana'),
        ("Himachal Pradesh", 'Himachal Pradesh'),
        ("Jammu & Kashmir", 'Jammu & Kashmir'),
        ("Jharkhand", 'Jharkhand'),
        ("Karnataka", 'Karnataka'),
        ("Kerala", 'Kerala'),
        ("Lakshadweep", 'Lakshadweep'),
        ("Madhya Pradesh", 'Madhya Pradesh'),
        ("Maharashtra", 'Maharashtra'),
        ("Manipur", 'Manipur'),
        ("Meghalaya", 'Meghalaya'),
        ("Mizoram", 'Mizoram'),
        ("Nagaland", 'Nagaland'),
        ("Odisha", 'Odisha'),
        ("Puducherry", 'Puducherry'),
        ("Punjab", 'Punjab'),
        ("Rajasthan", 'Rajasthan'),
        ("Sikkim", 'Sikkim'),
        ("Tamil Nadu", 'Tamil Nadu'),
        ("Telangana", 'Telangana'),
        ("Tripura", 'Tripura'),
        ("Uttarakhand", 'Uttarakhand'),
        ("Uttar Pradesh", 'Uttar Pradesh'),
        ("West Bengal", 'West Bengal'),
    )

    user = models.ForeignKey(
        User, related_name='orderaddress', on_delete=models.CASCADE)
    mobile = models.CharField(max_length=50, null=True)
    address = models.TextField()
    first_name = models.CharField(max_length=225, null=True, blank=True)
    last_name = models.CharField(max_length=225, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    alternate_mobile = models.CharField(max_length=10, null=True, blank=True)
    order = models.ForeignKey(
        CartOrder, related_name='orderaddress', on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    pincode = models.CharField(max_length=6, null=True)
    landmark = models.CharField(max_length=500, null=True, blank=True)
    locality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, null=True)

    class Meta:
        verbose_name_plural = '5. Order AddressBook'


class DeliveryOrderAddressBook(models.Model):
    STATE_CHOICES = (
        ("Andaman & Nicobar Islands", 'Andaman & Nicobar Islands'),
        ("Andhra Pradesh", 'Andhra Pradesh'),
        ("Arunachal Pradesh", 'Arunachal Pradesh'),
        ("Assam", 'Assam'),
        ("Bihar", 'Bihar'),
        ("Chandigarh", 'Chandigarh'),
        ("Chhattisgarh", 'Chhattisgarh'),
        ("Dadra & Nagar Haveli", 'Dadra & Nagar Haveli'),
        ("Daman and Diu", 'Daman and Diu'),
        ("Delhi", 'Delhi'),
        ("Goa", 'Goa'),
        ("Gujarat", 'Gujarat'),
        ("Haryana", 'Haryana'),
        ("Himachal Pradesh", 'Himachal Pradesh'),
        ("Jammu & Kashmir", 'Jammu & Kashmir'),
        ("Jharkhand", 'Jharkhand'),
        ("Karnataka", 'Karnataka'),
        ("Kerala", 'Kerala'),
        ("Lakshadweep", 'Lakshadweep'),
        ("Madhya Pradesh", 'Madhya Pradesh'),
        ("Maharashtra", 'Maharashtra'),
        ("Manipur", 'Manipur'),
        ("Meghalaya", 'Meghalaya'),
        ("Mizoram", 'Mizoram'),
        ("Nagaland", 'Nagaland'),
        ("Odisha", 'Odisha'),
        ("Puducherry", 'Puducherry'),
        ("Punjab", 'Punjab'),
        ("Rajasthan", 'Rajasthan'),
        ("Sikkim", 'Sikkim'),
        ("Tamil Nadu", 'Tamil Nadu'),
        ("Telangana", 'Telangana'),
        ("Tripura", 'Tripura'),
        ("Uttarakhand", 'Uttarakhand'),
        ("Uttar Pradesh", 'Uttar Pradesh'),
        ("West Bengal", 'West Bengal'),
    )
    user = models.ForeignKey(
        User, related_name='deliveryorderitem', on_delete=models.CASCADE, default='1')
    mobile = models.CharField(max_length=50, null=True)

    address = models.TextField()
    first_name = models.CharField(max_length=225, null=True, blank=True)
    last_name = models.CharField(max_length=225, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    alternate_mobile = models.CharField(max_length=10, null=True, blank=True)
    order = models.ForeignKey(
        CartOrder, related_name='deliveryorderitem', on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6, null=True)
    landmark = models.CharField(max_length=500, null=True, blank=True)
    locality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, null=True)

    vendor = models.CharField(max_length=500, null=True, blank=True)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    color = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=200, blank=True, null=True)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    paid_status = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        choices=status_choice, default='process', max_length=150)
    deliveryboy = models.ForeignKey(
        DeliveryBoy, related_name='deliveryorderitem', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Delivery Order AddressBook'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:25px; background-color:%s;"></div>' % (self.color))


# AddressBook
class UserAddressBook(models.Model):
    STATE_CHOICES = (
        ("Andaman & Nicobar Islands", 'Andaman & Nicobar Islands'),
        ("Andhra Pradesh", 'Andhra Pradesh'),
        ("Arunachal Pradesh", 'Arunachal Pradesh'),
        ("Assam", 'Assam'),
        ("Bihar", 'Bihar'),
        ("Chandigarh", 'Chandigarh'),
        ("Chhattisgarh", 'Chhattisgarh'),
        ("Dadra & Nagar Haveli", 'Dadra & Nagar Haveli'),
        ("Daman and Diu", 'Daman and Diu'),
        ("Delhi", 'Delhi'),
        ("Goa", 'Goa'),
        ("Gujarat", 'Gujarat'),
        ("Haryana", 'Haryana'),
        ("Himachal Pradesh", 'Himachal Pradesh'),
        ("Jammu & Kashmir", 'Jammu & Kashmir'),
        ("Jharkhand", 'Jharkhand'),
        ("Karnataka", 'Karnataka'),
        ("Kerala", 'Kerala'),
        ("Lakshadweep", 'Lakshadweep'),
        ("Madhya Pradesh", 'Madhya Pradesh'),
        ("Maharashtra", 'Maharashtra'),
        ("Manipur", 'Manipur'),
        ("Meghalaya", 'Meghalaya'),
        ("Mizoram", 'Mizoram'),
        ("Nagaland", 'Nagaland'),
        ("Odisha", 'Odisha'),
        ("Puducherry", 'Puducherry'),
        ("Punjab", 'Punjab'),
        ("Rajasthan", 'Rajasthan'),
        ("Sikkim", 'Sikkim'),
        ("Tamil Nadu", 'Tamil Nadu'),
        ("Telangana", 'Telangana'),
        ("Tripura", 'Tripura'),
        ("Uttarakhand", 'Uttarakhand'),
        ("Uttar Pradesh", 'Uttar Pradesh'),
        ("West Bengal", 'West Bengal'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=50, null=True)
    address = models.TextField()
    first_name = models.CharField(max_length=225, null=True, blank=True)
    last_name = models.CharField(max_length=225, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    alternate_mobile = models.CharField(max_length=10, null=True, blank=True)

    pincode = models.CharField(max_length=6, null=True)
    landmark = models.CharField(max_length=500, null=True, blank=True)
    locality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '6. AddressBook'


class UserDetail(models.Model):
    SEX_CHOICES = (("Male", 'Male'), ("Female", 'Female'), ("Other", 'Other'))
    STATE_CHOICES = (
        ("Andaman & Nicobar Islands", 'Andaman & Nicobar Islands'),
        ("Andhra Pradesh", 'Andhra Pradesh'),
        ("Arunachal Pradesh", 'Arunachal Pradesh'),
        ("Assam", 'Assam'),
        ("Bihar", 'Bihar'),
        ("Chandigarh", 'Chandigarh'),
        ("Chhattisgarh", 'Chhattisgarh'),
        ("Dadra & Nagar Haveli", 'Dadra & Nagar Haveli'),
        ("Daman and Diu", 'Daman and Diu'),
        ("Delhi", 'Delhi'),
        ("Goa", 'Goa'),
        ("Gujarat", 'Gujarat'),
        ("Haryana", 'Haryana'),
        ("Himachal Pradesh", 'Himachal Pradesh'),
        ("Jammu & Kashmir", 'Jammu & Kashmir'),
        ("Jharkhand", 'Jharkhand'),
        ("Karnataka", 'Karnataka'),
        ("Kerala", 'Kerala'),
        ("Lakshadweep", 'Lakshadweep'),
        ("Madhya Pradesh", 'Madhya Pradesh'),
        ("Maharashtra", 'Maharashtra'),
        ("Manipur", 'Manipur'),
        ("Meghalaya", 'Meghalaya'),
        ("Mizoram", 'Mizoram'),
        ("Nagaland", 'Nagaland'),
        ("Odisha", 'Odisha'),
        ("Puducherry", 'Puducherry'),
        ("Punjab", 'Punjab'),
        ("Rajasthan", 'Rajasthan'),
        ("Sikkim", 'Sikkim'),
        ("Tamil Nadu", 'Tamil Nadu'),
        ("Telangana", 'Telangana'),
        ("Tripura", 'Tripura'),
        ("Uttarakhand", 'Uttarakhand'),
        ("Uttar Pradesh", 'Uttar Pradesh'),
        ("West Bengal", 'West Bengal'),
    )
    user = models.OneToOneField(
        User, related_name="customer", on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=225, null=True, blank=True)
    last_name = models.CharField(max_length=225, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    dob = models.DateField(null=True)
    photo = models.ImageField(default='user.png', upload_to='user_photos/')
    mobile = models.CharField(max_length=12, null=True)
    alternate_mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField()
    pincode = models.CharField(max_length=6, null=True)
    landmark = models.CharField(max_length=500, null=True, blank=True)
    locality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, null=True)
    Gender = models.CharField(max_length=6, choices=SEX_CHOICES, null=True)

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
        verbose_name_plural = '7. User Detail'
