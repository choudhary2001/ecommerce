import calendar
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Max, Min, Count, Avg
from django.urls.base import is_valid_path
from product.models import Category, Brand, Product,  Banner
from django.template.loader import render_to_string
from vendor.models import Vendor
from django.http import JsonResponse, HttpResponse, request, response
from .forms import ReviewAdd
from .models import OrderAddressBook, ProductReview, UserDetail, Wishlist, UserAddressBook, CartOrderItems, CartOrder, DeliveryOrderAddressBook
from .forms import SignupForm, ReviewAdd, AddressBookForm, UserDetailForm, RecivedForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
# paytm
import json
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
# Create your views here.
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from .utilities import notify_customer, notify_vendor
from django.views.decorators.csrf import csrf_exempt
from .paytm import generate_checksum, verify_checksum


def home(request):
    if request.user.is_staff:
        return redirect("vendor_admin")
    else:
        pass

    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/index.html', {'vendors': vendors, 'categories': categories})


# category
def category_list(request):
    data = Category.objects.all().order_by('-id')
    return render(request, 'main/category_list.html', {'data': data})


def brands_list(request):
    brands = Brand.objects.all().order_by('-id')
    return render(request, 'main/brands_list.html', {'brands': brands})


# Product List
def product_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:3]

    min_price = Product.objects.aggregate(Min('price'))
    max_price = Product.objects.aggregate(Max('price'))
    return render(request, 'main/product_list.html',
                  {
                      'data': data,
                      'total_data': total_data,
                      'min_price': min_price,
                      'max_price': max_price,

                  }
                  )

# Product List According to Category


def category_product_list(request, cat_id):
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by('-id')

    return render(request, 'main/category_product_list.html', {
        'data': data,

    })

# Product List According to Brand


def brand_product_list(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    return render(request, 'main/brand_product_list.html', {
        'data': data,

    })


# Product Detail
def product_detail(request, slug, id):
    product = Product.objects.get(id=id)

    related_products = Product.objects.filter(
        category=product.category).exclude(id=id)[:4]

    reviewForm = ReviewAdd()

    # Check
    canAdd = True

    # End

    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'main/product_detail.html', {'data': product, 'related': related_products, 'reviewForm': reviewForm, 'canAdd': canAdd, 'reviews': reviews, 'avg_reviews': avg_reviews})


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

# Load More


def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('main/ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t}
                        )
# search


def search(request):
    q = request.GET['q']
    data = Product.objects.filter(Q(title__icontains=q) | Q(
        details__icontains=q)).order_by('-id')

    return render(request, 'main/search.html', {'data': data})

# Save Review

@login_required
def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.first_name,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})


# Add to cart
def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'price_not': request.GET['price_not']
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})

# Cart List Page


def cart_list(request):
    total_amt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
        return render(request, 'main/cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    else:
        return render(request, 'main/cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})


# Delete Cart Item
def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('main/ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# Wishlist

def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('main/ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# Signup Form
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = User.objects.filter(username=username).first()
            if username.isdigit():
                UserDetail(user=user, mobile=username).save()
            else:
                user.email = username
                user.save()
                UserDetail(user=user).save()
                messages.success(request, f'Account is Created for {username}')
            
            return redirect('profile')
    else:
        form = SignupForm
    return render(request, 'main/registration/signup.html', {'form': form})


# Checkout
@login_required
def checkoutaddress(request):
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
            
    else:
        form = AddressBookForm
    address = UserAddressBook.objects.filter(
        user=request.user, status=True).first()
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/user/checkoutaddress.html', {'address': address, 'addbook': addbook, 'form': form})


@login_required
def cashcheckout(request):
    total_amt = 0
    totalAmt = 0
    msg = None
    msg = None

    if 'cartdata' in request.session:

        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty'])*float(item['price'])

        # Order
        order = CartOrder.objects.create(
            user=request.user,
            vendor=Product.objects.filter(id=p_id).first().vendor,
            total_amt=totalAmt,
            payment='cashondelivery',

        )

        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
            # OrderItems
            items = CartOrderItems.objects.create(
                order=order,
                user=request.user,
                vendor=Product.objects.filter(id=p_id).first().vendor,
                color=Product.objects.filter(id=p_id).first().color,
                size=Product.objects.filter(id=p_id).first().size,

                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price']),


            )
            
            # End

        for p_id, item in request.session['cartdata'].items():
            total_am = int(item['qty'])*float(item['price'])
            orderaddress = DeliveryOrderAddressBook.objects.create(

                order=order,


                first_name=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().first_name,
                last_name=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().last_name,
                email=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().email,
                mobile=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().mobile,
                alternate_mobile=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().alternate_mobile,
                address=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().address,
                pincode=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().pincode,
                landmark=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().landmark,
                locality=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().locality,
                city=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().city,
                state=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().state,
                vendor=Product.objects.filter(
                    id=p_id).first().vendor.shop_Name,

                color=Product.objects.filter(id=p_id).first().color,
                size=Product.objects.filter(id=p_id).first().size,

                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price']),


            )

            

        for p_id, item in request.session['cartdata'].items():
            total_amt = int(item['qty'])*float(item['price'])
            address = OrderAddressBook.objects.create(

                order=order,
                invoice_no='INV-'+str(order.id),
                user=request.user,
                first_name=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().first_name,
                last_name=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().last_name,
                email=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().email,
                mobile=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().mobile,
                alternate_mobile=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().alternate_mobile,
                address=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().address,
                pincode=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().pincode,
                landmark=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().landmark,
                locality=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().locality,
                city=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().city,
                state=UserAddressBook.objects.filter(
                    user=request.user, status=True).first().state

            )

    
    # Process Payment
    return redirect('my_orders')



@login_required
def checkout(request):
    total_amt = 0
    totalAmt = 0
    msg = None
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
            return redirect('checkout')
    else:
        form = AddressBookForm
    address = UserAddressBook.objects.filter(
        user=request.user, status=True).first()
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    if 'cartdata' in request.session:
        if address:

            for p_id, item in request.session['cartdata'].items():
                totalAmt += int(item['qty'])*float(item['price'])

        # Order
            order = CartOrder.objects.create(
                user=request.user,
                vendor=Product.objects.filter(id=p_id).first().vendor,
                total_amt=totalAmt,

            )
            for p_id, item in request.session['cartdata'].items():
                total_amt += int(item['qty'])*float(item['price'])
            # OrderItems
                items = CartOrderItems.objects.create(
                    order=order,
                    user=request.user,
                    vendor=Product.objects.filter(id=p_id).first().vendor,
                    color=Product.objects.filter(id=p_id).first().color,
                    size=Product.objects.filter(id=p_id).first().size,

                    invoice_no='INV-'+str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty'])*float(item['price']),


                )
                notify_customer(items)

            # End

            for p_id, item in request.session['cartdata'].items():
                total_am = int(item['qty'])*float(item['price'])
                orderaddress = DeliveryOrderAddressBook.objects.create(

                    order=order,


                    first_name=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().first_name,
                    last_name=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().last_name,
                    email=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().email,
                    mobile=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().mobile,
                    alternate_mobile=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().alternate_mobile,
                    address=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().address,
                    pincode=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().pincode,
                    landmark=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().landmark,
                    locality=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().locality,
                    city=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().city,
                    state=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().state,


                    vendor=Product.objects.filter(
                        id=p_id).first().vendor.shop_Name,

                    color=Product.objects.filter(id=p_id).first().color,
                    size=Product.objects.filter(id=p_id).first().size,

                    invoice_no='INV-'+str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty'])*float(item['price']),


                )

            for p_id, item in request.session['cartdata'].items():
                total_amt = int(item['qty'])*float(item['price'])
                address = OrderAddressBook.objects.create(

                    order=order,
                    invoice_no='INV-'+str(order.id),
                    user=request.user,
                    first_name=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().first_name,
                    last_name=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().last_name,
                    email=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().email,
                    mobile=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().mobile,
                    alternate_mobile=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().alternate_mobile,
                    address=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().address,
                    pincode=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().pincode,
                    landmark=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().landmark,
                    locality=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().locality,
                    city=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().city,
                    state=UserAddressBook.objects.filter(
                        user=request.user, status=True).first().state

                )

        else:
            if request.method == 'POST':
                form = AddressBookForm(request.POST)
                if form.is_valid():
                    saveForm = form.save(commit=False)
                    saveForm.user = request.user
                    if 'status' in request.POST:
                        UserAddressBook.objects.update(status=False)
                    saveForm.save()
                    msg = 'Data has been saved'
                    return redirect('checkout')
            else:
                form = AddressBookForm
            return render(request, 'main/user/add-address.html', {'form': form, 'msg': msg})

        # cart_data=request.session['cartdata']
        #del request.session['cartdata'][p_id]
        # request.session['cartdata']=cart_data
    
        # Process Payment
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
                ('MID', settings.PAYTM_MERCHANT_ID),
                ('ORDER_ID', str(address.order.id)),
                ('CUST_ID', str(address.user.username)),
                ('TXN_AMOUNT', str(items.total)),
                ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
                ('WEBSITE', settings.PAYTM_WEBSITE),
                # ('EMAIL', request.user.email),
                # ('MOBILE_N0', '9911223388'),
                ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
                ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
                # ('PAYMENT_MODE_ONLY', 'NO'),
                )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)


    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'main/redirect.html', context=paytm_params)



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            if 'cartdata' in request.session:

                for p_id, item in request.session['cartdata'].items():

                    order = CartOrder.objects.update(
                        payment='paid',
                        paid_status='True',

                        )
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'main/payment-fail.html', context=received_data)
        return render(request, 'main/payment-successful.html', context=received_data)


@csrf_exempt
def payment_done(request):
    returnData = request.POST
    return render(request, 'main/payment-success.html', {'data': returnData})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'main/payment-fail.html')


# User Dashboard


def my_dashboard(request):
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values(
        'month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'main/user/dashboard.html', {'monthNumber': monthNumber, 'totalOrders': totalOrders})

# My Orders

@login_required
def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/user/orders.html', {'orders': orders})

@login_required
def my_invoice(request, id):
    user = request.user
    address = user.orderaddress.get(id=id)
    product = user.orderitem.get(id=id)
    pay = product.order

    return render(request, 'main/user/invoice.html', {'product': product, 'address': address, 'pay': pay})

# Order Detail

@login_required
def my_order_items(request, id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    orderaddress = OrderAddressBook.objects.filter(order=order)
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/user/order-items.html', {'orderitems': orderitems, 'orderaddress': orderaddress, 'orders': orders})


@login_required
def edit_customerorder(request, id):
    user = request.user
    product = user.orderitem.get(id=id)
    msg = None
    if request.method == 'POST':
        form = RecivedForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            msg = 'Status updated'
            return redirect('my_orders')
    else:
        form = RecivedForm(instance=product)
    return render(request, 'main/user/edit_order.html', {'form': form, 'msg': msg})
# Wishlist


def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(
        product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


# My Wishlist
def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/user/wishlist.html', {'wlist': wlist})


# My Reviews
def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/user/reviews.html', {'reviews': reviews})

# My AddressBook


def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/user/addressbook.html', {'addbook': addbook})

# Save addressbook


def save_address(request):
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm
    return render(request, 'main/user/add-address.html', {'form': form, 'msg': msg})

# Activate address


def activate_address(request):
    a_id = str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool': True})

# Edit Profile


def edit_userprofile(request):

    if request.user.customer:
        user = request.user.customer
        if request.method == 'POST':
            form = UserDetailForm(
                request.POST, request.FILES, instance=request.user.customer)
            if form.is_valid():
                form.save()
                messages.success(request, f'Account is Updated')
                return redirect('profile')
        else:
            form = UserDetailForm(instance=request.user.customer)
        return render(request, 'main/user/edit-profile.html', {'form': form, 'title': 'Update User Profile'})

    else:
        return redirect("/")

# Update addressbook


def update_address(request, id):
    address = UserAddressBook.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm(instance=address)
    return render(request, 'main/user/update-address.html', {'form': form, 'msg': msg})


@login_required
def profile(request):
    if request.user.is_staff:
        return redirect("update_vendor")
    else:
        pass

    customer = request.user

    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')

    orders = CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values(
        'month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'main/user/profile.html', {'customer': customer, 'reviews': reviews, 'wlist': wlist, 'monthNumber': monthNumber, 'totalOrders': totalOrders})


def account(request):
    account = request.user

    return render(request, 'main/accounts.html', {'account': account})
