from django.contrib import admin
from .models import ProductReview,Wishlist,UserAddressBook,UserDetail, CartOrder, CartOrderItems, OrderAddressBook, DeliveryOrderAddressBook

# Register your models here.


# Order


class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Wishlist)




class UserDetailAdmin(admin.ModelAdmin):
	list_display=(            
            'user',
			'first_name',
			'last_name',
			'email',
			'photo',
			'dob',
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
			'Gender',)
admin.site.register(UserDetail,UserDetailAdmin)



# Order
class CartOrderAdmin(admin.ModelAdmin):
	list_editable=('paid_status','order_status', 'vendor', 'deliveryboy')
	list_display=('user',  'vendor','total_amt', 'payment','paid_status','status','order_dt','order_status', 'deliveryboy')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
	list_editable=('order_status','deliveryboy')
	list_display=('user', 'vendor','invoice_no','item','image_tag','qty', 'color' ,  'size','price','total','order_status', 'deliveryboy')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)




class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=(           
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
			'state','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)

class OrderAddressBookAdmin(admin.ModelAdmin):
	list_display=(       
		   'user',    
		   'first_name',
		   'last_name',
			'invoice_no',
			'order',
            'email',
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state')
admin.site.register(OrderAddressBook,OrderAddressBookAdmin)


class DeliveryOrderAddressBookAdmin(admin.ModelAdmin):
	
	list_display=(       
		    
			'vendor',
			
		   'first_name',
		   'last_name',
			'invoice_no',
            'email',
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
			'item','image_tag','qty', 'color' ,  'size','price','total',
			'paid_status','status','order_dt',
			)
	
admin.site.register(DeliveryOrderAddressBook,DeliveryOrderAddressBookAdmin)
