
from os import name
import django
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import request
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor
from .forms import ProductForm,  VendorProfileForm, VendorSignUpForm, CartOrderItemForm, CartOrderForm
from product.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, request
from django.db.models.query_utils import  Q
from product.models import Banner, Category
# Create your views here.



# Signup for Vendor
def become_vendor(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = VendorSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                shop = form.cleaned_data.get('shop')
                gst = form.cleaned_data.get('gst')
                usr = User.objects.filter(username=username).first()
                usr.is_staff = True
                usr.save()
                if username.isdigit():
                    Vendor(user=usr, mobile=username, gst_Number=gst,
                           shop_Name=shop, name=username).save()
                else:
                    usr.email = username
                    usr.save()
                    Vendor(user=usr, gst_Number=gst, shop_Name=shop).save()
                messages.success(request, f'Account is Created for {username}')
                return redirect('/')
        else:
            form = VendorSignUpForm()
    return render(request, 'vendor/become_vendor.html', {'form': form, 'title': 'Become a vendor'})


def update_vendor(request):

    if request.user.vendor:
        vendor = request.user.vendor
        if request.method == 'POST':
            form = VendorProfileForm(request.POST, request.FILES, instance=request.user.vendor)
            if form.is_valid():
                form.save()
                messages.success(request, f'Account is Updated')
                return redirect('vendor_admin')
        else:
            form = VendorProfileForm(instance=request.user.vendor)
        return render(request, 'vendor/update_vendor.html', {'form': form, 'title': 'Update Vendor Profile'})

    else:
        return redirect("/")


@login_required
def vendor_admin(request):
    if request.user.is_staff:
	    pass
    vendor = request.user.vendor
    products = vendor.products.all().order_by('-id')
    orders = vendor.orderitem.all()
    userdetail = vendor.userorder.all()


    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders, 'userdetail': userdetail})


@login_required
def order(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orderitem.all().order_by('-id')
    userdetail = vendor.userorder.all().order_by('-id')

    return render(request, 'vendor/order.html', {'orders': orders, 'userdetail': userdetail})

@login_required
def order_search(request):
    q=request.GET['l']
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orderitem.all().order_by('-id')
    data=vendor.orderitem.filter(Q(item__icontains=q) | Q(invoice_no__icontains=q)).order_by('-id')

    return render(request,'vendor/search.html',{'data':data})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    vendor = request.user.vendor
    product = vendor.products.get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm(instance=product)

    return render(request, 'vendor/edit_product.html', {'form': form, 'product': product})


@login_required
def edit_order(request, pk):
    vendor = request.user.vendor
    product = vendor.orderitem.get(pk=pk)
    product1 = product.order
    if request.method == 'POST':
        form = CartOrderItemForm(request.POST,  instance=product)
        form1 = CartOrderForm(request.POST,  instance=product1)

        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()

            return redirect('/')
    else:
        form = CartOrderItemForm(instance=product)
        form1 = CartOrderForm(instance=product1)

    return render(request, 'vendor/edit_order.html', {'form': form,'form1': form1, 'product': product})


def vendor_account(request):
    vendor = request.user

    return render(request, 'vendor/vendordetail.html', {'vendor': vendor})


def vendors(request):
    vendor = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendor': vendor})


def vendor(request, vendor_id):
    vendo =  Vendor.objects.get(pk=vendor_id)
    vendor = vendo.products.all().order_by('-id')
    return render(request, 'vendor/vendor.html', {'vendor': vendor, 'vendo':vendo})

# Filter Data


def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(price__gte=minPrice)
    allProducts = allProducts.filter(price__lte=maxPrice)
    if len(colors) > 0:
        allProducts = allProducts.filter(color__id__in=colors).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(
            category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(size__id__in=sizes).distinct()
    t = render_to_string('main/ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})
