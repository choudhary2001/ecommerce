from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
import math, random

@login_required
def order(request):
    deliveryboy = request.user.deliveryboy
    orders = deliveryboy.orderitem.all().order_by('-id')
    userdetail = deliveryboy.userorder.all().order_by('-id')

    return render(request, 'deliveryboy/order.html', {'orders': orders, 'userdetail': userdetail})
