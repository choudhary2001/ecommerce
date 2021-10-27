from django.contrib import admin
from .models import DeliveryBoy
# Register your models here.

class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display=( 'user', 'first_name', 'last_name','adhar_Number' ,'image_tag')
admin.site.register(DeliveryBoy, DeliveryBoyAdmin)
