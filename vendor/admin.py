from django.contrib import admin
from .models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display=( 'user', 'gst_Number', 'shop_Name','image_tag')
admin.site.register(Vendor, VendorAdmin)

