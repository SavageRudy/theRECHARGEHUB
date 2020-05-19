from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Combo,Talktime,Internet
from . import models
from .forms import RegisterForm,ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        context = {
            "combo" : Combo.objects.all(),
            "net" : Internet.objects.all(),
            "talk" : Talktime.objects.all(),
        }
        return render(request,"main/index.html",context)
    else:
        context = {
            "combo" : Combo.objects.all(),
            "net" : Internet.objects.all(),
            "talk" : Talktime.objects.all(),
        }
        return render(request,"main/index.html",context)         
    

@transaction.atomic
def register(request):
    if request.method == "GET":
        form = RegisterForm()
        profile_form = ProfileForm()
        context={
            "form" : form,
            "profile_form" : profile_form
        }
        return render(request,"main/register.html",context)

    elif request.method == "POST":
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)

        profile_form.is_valid()
        form.is_valid()

        """if form.is_valid():"""
        user = form.save()
        user.profile.num = profile_form.cleaned_data['num']
        user.save()

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect('/')
        """else:
            form = RegisterForm()
            profile_form = ProfileForm()
            context={
            "form" : form,
            "profile_form" : profile_form
            }
            return render(request, "main/register.html", context)   """ 

def login_request(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('/login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login') 

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/login")  

def browse(request):
        id = request.POST.get("pack_id")
        db = request.POST.get("db_name")
        fn = getattr(models,db)
        result =  fn.objects.all().filter(id = id).values()[0]
        context = {
            "result" : result,
            "db" : db
        }
        
        return render(request,"main/browse.html",context) 

@login_required(login_url='/login')
def checkout(request):
    recipient_list = []
    subject = 'Confirmation'
    message = ' Your mobile recharge has been successfull.'
    email_from = settings.EMAIL_HOST_USER


    
    recipient_list.append(request.user.email)
    
    send_mail( subject = subject, message = message, from_email= email_from,recipient_list= recipient_list, fail_silently=False)
    context = {
       'msg' : 'Email has been sent'
    }
    return render(request,"main/checkout.html",context)

@login_required(login_url='/login')
def profile(request):
    p_list={}
    p_list['name']=request.user.username
    p_list['email']=request.user.email
    p_list['num'] = request.user.profile.num
    context = {
        'profile' : p_list
    }
    return render(request,"main/profile.html",context)

def combo(request):
    context={
        'combo' : Combo.objects.all(),
    }
    return render(request,"main/combo.html",context)

def internet(request):
    context={
        'net' : Internet.objects.all(),
    }
    return render(request,"main/internet.html",context)

def talk(request):
    context={
        'talk' : Talktime.objects.all(),
    }
    return render(request,"main/talk.html",context)





