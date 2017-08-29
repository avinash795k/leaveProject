from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.
def home(request):
    if not request.user.is_authenticated():
        return redirect('/')

    return render(request, 'userpanel/base.html')


def login_user(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        if request.method=='POST':
            form = FormLogin(request.POST)
            if form.is_valid():
                username = request.POST.get("username")
                password = request.POST.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)
                    return redirect('/home')
            form = FormLogin()
            return render(request, 'userpanel/login_page.html', {"form":form,"error":"Invalid Username or Password"})
        else:
            form = FormLogin()
            return render(request, 'userpanel/login_page.html', {"form":form})


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')