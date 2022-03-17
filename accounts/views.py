from asyncio.windows_events import NULL
import uuid
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, auth
from friends.models import Profile
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail
import datetime

# Create your views here.

def index_register(request):
    if (request.method == "POST"):
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['Email']
        password = request.POST['password']
        day = request.POST['day']
        month = request.POST['month']
        year = request.POST['year']
        gender = request.POST['gender']
        city = request.POST['city']
        country = request.POST['country']

        if(User.objects.filter(username=username).exists()):
            messages.info(request,'Username is not available')
            return HttpResponseRedirect('index-register')
        elif(User.objects.filter(email=email).exists()):
            messages.info(request,'Email is already taken')
            return HttpResponseRedirect('index-register')
        else:
            year = int(year)
            day = int(day)
            month = int(month)
            x = datetime.datetime(year, month, day)
            user=User.objects.create_user(username=username,password=password,email=email,first_name=firstname,last_name=lastname)
            #user.save()
            profile = Profile(user=user,gender=gender,city=city,country=country,dateOfBirth=x,image='pics/avatardefault_92824_2gthZ14.png')
            profile.save()
            return HttpResponseRedirect('/index-register')

        return HttpResponseRedirect('/')
    else:
        return render(request,'index-register.html')


def login(request) :
    username = request.POST['my-username']
    password = request.POST['my-password']
    user = authenticate(request, username=username, password=password)
    print(user)
    # https://docs.djangoproject.com/en/1.11/topics/auth/default/#django.contrib.auth.authenticate
    if user is not None :
        print(user)
        request.session["username"] = username #sets the exp. value of the session 
        return HttpResponseRedirect('/')
    messages.info(request, "User name Or Password is not Matched")
    return HttpResponseRedirect('index-register')

def password_reset(request):
   
    if(False == (User.objects.filter(email = request.POST['email']).exists())):
            messages.info(request,'Email is not Valid')
            return HttpResponseRedirect('index-register')
    test = uuid.uuid4()
    print(test)
    u = User.objects.get(email = request.POST['email'])
    u.set_password(str(test))
    u.save()
    subject = 'Password Reset Link'
    message = 'Hello Here is your one password reset token ' + str(u.id)+"@"+ str(test)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.POST['email']]
    send_mail( subject, message, email_from, recipient_list )

    return HttpResponseRedirect('password-change')

def password_change(request) :
    if(request.method == "POST") :
        token = request.POST['token']
        token = token.split("@")
        id = int(token[0])
        password = request.POST['password']
        confirm_password = request.POST['cpassword']
        user = User.objects.get(id = id)
        if(user.check_password(token[0])):
            messages.info(request, "token number is not valid")
            return HttpResponseRedirect('password-change')
        if ( password != confirm_password) :
            messages.info(request, "Password and Confirm Password not matched it must be same")
            return HttpResponseRedirect('password-change')
        user.set_password(password)
        user.save()
        return HttpResponseRedirect('index-register')
    return render(request,"password-reset.html")