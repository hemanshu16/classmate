from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from friends.models import Profile
from django.contrib import messages
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
            return redirect('index-register')
        elif(User.objects.filter(email=email).exists()):
            messages.info(request,'Email is already taken')
            return redirect('index-register')
        else:
            year = int(year)
            day = int(day)
            month = int(month)
            x = datetime.datetime(year, month, day)
            user=User.objects.create_user(username=username,password=password,email=email,first_name=firstname,last_name=lastname)
            #user.save()
            profile = Profile(user=user,gender=gender,city=city,country=country,dateOfBirth=x)
            profile.save()
            return redirect('/')

        return redirect('/')
    else:
        return render(request,'index-register.html')