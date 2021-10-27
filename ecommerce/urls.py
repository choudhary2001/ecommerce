"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from vendor.views import order_search
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/', include('vendor.urls')),
    path('', include('main.urls')),
    path('deliveryboy/', include('delivery.urls')),
    
    path("accounts/login/", auth_views.LoginView.as_view(template_name='main/registration/login.html', redirect_authenticated_user=True), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("accounts/password-reset/", auth_views.PasswordResetView.as_view(template_name='main/registration/password_reset_form.html'), name="password_reset"),
    path("accounts/password-change/", auth_views.PasswordChangeView.as_view(template_name='main/registration/password_change_form.html'), name="password_change"),
    path("accounts/password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='main/registration/password_reset_done.html'), name="password_reset_done"),
    path("accounts/password-change/done/", auth_views.PasswordChangeDoneView.as_view(template_name='main/registration/password_change_done.html'), name="password_change_done"),   
    path("accounts/password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='main/registration/password_reset_confirm.html'), name="password_reset_confirm"),
    path("accounts/password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='main/registration/password_reset_complete.html'), name="password_reset_complete"),
    path('ordersearch',order_search,name='ordersearch'),
    path('accounts/', include('allauth.urls')),

 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
