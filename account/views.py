from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.contrib.auth.models import User, Group
from .models import Member
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import time
import random
import string

#self functions

def validate_input(inp):
    if(inp is None):
        return False
    if(len(inp) != len(inp.strip())):
        return False
    if(len(inp.split()) != 1):
        return False
    return True

def createcode():
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return code

def index(request):
    return HttpResponse("Hello, world. You're at Home.")

def signup(request):
    context = {
        "fields" : [
            [
                {
                    'name' : 'Entry Number',
                    'id' : 'username',
                    'size' : '12',
                    'icon' : 'account_circle'
                }                
            ]   
        ]
    }
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password_1 = request.POST.get('password1')
        password_2 = request.POST.get('password2')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname','')
        gender = request.POST.get('gender')
        if(validate_input(username) == False or username.isalnum() == False):
            context = {'error_message' : "Invalid Entry Number"}
        elif((validate_input(password_1) and validate_input(password_2)) == False ):
            context = {'error_message' : "Invalid Password"}
        elif(validate_input(fname) == False or (fname+lname).isalpha() == False ):
            context = {'error_message' : "Invalid Name"}
        elif(gender not in ['Male', 'Female', 'Other'] ):
            context = {'error_message' : "Invalid Gender"}
        elif(password_1 != password_2):
            context = {'error_message' : "Password not match"}
        elif(len(password_1) < 8):
            context = {'error_message' : "Password less than 8 chars"}
        else:
            request.session['username'] = username
            request.session['password'] = password_1
            request.session['fname'] = fname
            request.session['lname'] = lname
            request.session['gender'] = gender
            request.session['started'] = time.time()
            request.session['code_entered'] = 0
            verf_code = createcode()
            request.session['verf_code'] = verf_code
            user_email = username + "@iitjammu.ac.in"
            email_body = render_to_string('account/signup_otp_email.html', {'username' : username, 'verf_code' : verf_code })
            email = EmailMessage(
                subject= 'Verification Code',
                body = email_body,
                from_email = 'dashboard@iamabhishek.co',
                to = [user_email],
            )
            email.content_subtype = "html"
            email.send()
            return HttpResponseRedirect(reverse_lazy('account:verify'))
    return render(request, 'account/signup.html', context)

def signup_verify(request):

    if((time.time() - request.session.get('started',0)) < 180 and request.session.get('code_entered',100) < 2):
        context = {}
        if(request.method == "POST"):
            request.session['code_entered'] = request.session.get('code_entered') + 1
            verf_code = request.POST.get('verf_code','')
            code = request.session.get('verf_code','')
            fname = request.session.get('fname')
            lname = request.session.get('lname')
            gender = request.session.get('gender')
            if(code != "" and code == verf_code):
                username = request.session['username']
                password = request.session['password']
                user=Member.objects.create_user(
                    username= username , 
                    password= password,
                    email = username + "@iitjammu.ac.in" ,
                    first_name = fname,
                    last_name = lname,
                    gender = gender,
                )
                gru = Group.objects.get_or_create(name='members')[0] 
                gru.user_set.add(user)
                del request.session['code_entered']
                del request.session['username']
                del request.session['password']
                del request.session['verf_code']
                del request.session['fname'] 
                del request.session['lname'] 
                del request.session['gender']
                return HttpResponse("done")
            else:
                context = {
                    'error_message' : "Wrong Code"
                }
        return render(request, 'account/signup_otp.html')
    else:
        return redirect('/Signup/')
        #return render(request, 'account/signup_otp.html')
    


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
                'error_message' : "Wrong ID or Password"
            }
    except(KeyError):
        if(request.user.is_authenticated):
            return redirect(ret_page)
        context = {'args':ret_param}
        return render(request, 'account/login.html', context)
    else:
        return render(request, 'account/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponse("logged out")

@login_required
def home_view(request):
    return HttpResponse("this is home")
 
def forget_view(request):
    return auth_views.PasswordResetView.as_view(
        template_name = 'account/forget_password.html',
        email_template_name = 'account/reset_email.html',
        html_email_template_name = 'account/reset_email.html',
        from_email = "dashboard@iamabhishek.co",
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

