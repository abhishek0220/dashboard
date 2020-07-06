from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index(request):
    return HttpResponse("Hello, world. You're at Home.")

def signup(request):
    return render(request, 'account/signup.html')

def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            context = {
                'error_message' : "wrong"
            }
    except(KeyError):
        if(request.user.is_authenticated):
            return redirect('/home/')
        context = {}
        return render(request, 'account/login.html', context)
    else:
        return render(request, 'account/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponse("logged out")

@login_required
def home_view(request):
    return HttpResponse("this is home")

