# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
import random
from bestoon import settings
import string
import os
import requests
from django.views.decorators.csrf import csrf_exempt
import smtplib,ssl
from web.models import User , Token , Expense,Income,Passwordresetcodes
from datetime import datetime
from django.contrib.auth.hashers import make_password
# Create your views here.


@csrf_exempt
def submit_income(request):
    this_token = request.POST["token"]
    this_user = User.objects.filter(token__token = this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    else:
        date = request.POST['date']
    Expense.objects.create(user=this_user,amount = request.POST["amount"],text = request.POST["text"],date=date)

    return JsonResponse({
        'status' : 'ok',
    },encoder= JSONEncoder)

@csrf_exempt
def submit_expense(request):
    this_token = request.POST["token"]
    this_user = User.objects.filter(token__token = this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    else:
        date = request.POST['date']
    Expense.objects.create(user=this_user,amount = request.POST["amount"],text = request.POST["text"],date=date)

    return JsonResponse({
        'status' : 'ok',
    },encoder= JSONEncoder)

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

def register(request):
    if request.POST.__contains__('requestcode'): #form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        if User.objects.filter(email = request.POST['email']).exists(): # duplicate email
            context = {'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)

        if not User.objects.filter(username = request.POST['username']).exists(): #if user does not exists
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            newuser = User.objects.create(username=username, password=password,email=email)
            this_token = random_str(48)
            token = Token.objects.create(user=newuser, token=this_token)
            context = {'message': 'اکانت شما فعال شد. لاگین کنید - البته اگر دوست داشتی و توکن شما {}'.format(this_token)}
            return render(request, 'login.html', context)
        else:
            context = {'message': 'شما قبلا ثبت نام کرده اید'}
            return render(request, 'login.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)

def index(request):
    contex = {}
    return render(request,'index.html',contex)