from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls.conf import include

urlpatterns = [
    path('', views.home, name='home'),
    path('search',views.search,name='search'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    
    path('category-list', views.category_list, name='category-list'),
    path('brands-list', views.brands_list, name='brands-list'),
    path('product-list', views.product_list, name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('brand-product-list/<int:brand_id>',views.brand_product_list,name='brand-product-list'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('accounts/signup',views.signup,name='signup'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    # User Section Start
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    path('edit-customerorder/<int:id>/', views.edit_customerorder, name='edit_customerorder'),
    path('checkout',views.checkout,name='checkout'),
    path('cashcheckout',views.cashcheckout,name='cash_checkout'),
   
    path('checkout-address',views.checkoutaddress,name='checkout_address'),
    # End
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('callback/', views.callback, name='callback'),

    # Wishlist
    path('add-wishlist',views.add_wishlist, name='add_wishlist'),
    
    path('my-wishlist',views.my_wishlist, name='my_wishlist'),
    # My Reviews
    path('my-reviews',views.my_reviews, name='my-reviews'),
    # My AddressBook
    path('my-addressbook',views.my_addressbook, name='my-addressbook'),
    path('add-address',views.save_address, name='add-address'),
    path('activate-address',views.activate_address, name='activate-address'),
    path('update-address/<int:id>',views.update_address, name='update-address'),
    path('edit-userprofile',views.edit_userprofile, name='edit-userprofile'),
  
    path('account', views.account, name='account' ),
    path('invoice/<int:id>', views.my_invoice, name='my_invoice' ),
    path('accounts/profile/',views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    