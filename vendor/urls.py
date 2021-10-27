from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor-admin/', views.vendor_admin, name='vendor_admin'),
    path('vendor-order/', views.order, name='vendor_order'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('edit-order/<int:pk>/', views.edit_order, name='edit_order'),
    path('update-vendor/', views.update_vendor, name='update_vendor'),
    path('vendor-account', views.vendor_account, name='vendor_account' ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='vendor/login.html'), name='vendor_login'),
    path('', views.vendors, name='vendors'),
    
    path('<str:vendor_id>/', views.vendor, name='vendor'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)