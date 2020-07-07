from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

def index(request):
    return HttpResponse("Hello, world. You're at Home.")

def signup(request):
    return render(request, 'account/signup.html')

def login_view(request):
    ret_page = request.GET.get('next', '')
    ret_param = ""
    if(ret_page != ''):
        ret_param = "?next=" + ret_page
    if(ret_page == ''):
        ret_page = '/home/'
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(ret_page)
        else:
            context = {
                'args':ret_param,
                'error_message' : "wrong"
            }
    except(KeyError):
        if(request.user.is_authenticated):
            return redirect(ret_page)
        context = {'args':ret_param}
        return render(request, 'account/login.html', context)
    else:
        return render(request, 'account/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponse("logged out")

@login_required
def home_view(request):
    return HttpResponse("this is home")

def send_email(request):
    subject = "check"
    message = "check mail from developer dashboard"
    from_email = settings.EMAIL_HOST_USER
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['abhishekchaudhary0220@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')
    
def forget_view(request):
    return auth_views.PasswordResetView.as_view(
        template_name = 'account/forget_password.html',
        email_template_name = 'account/reset_email.html',
        success_url =reverse_lazy('account:email_sent')
    )(request)

def email_sent(request):
    return auth_views.PasswordResetDoneView.as_view(
        template_name = 'account/forget_done.html'
    )(request)

def password_change(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view(
        template_name = 'account/reset_link.html'
    )(request, uidb64, token)
