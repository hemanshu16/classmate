from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from friends.models import Profile

# Create your views here.

def index(request) :
    return render(request,'index.html')

# def index_register(request):
#    return render(request, 'index-register.html')

def edit_profile_basic(request,username):
    flag = 0
    print(request.session["username"])
    if request.session["username"] == username:
        flag = 1

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user_id=user.id)
    return render(request, 'edit-profile-basic.html', {'flag':flag,'user':user,'profile':profile})

def edit_profile_interests(request,username):
    flag = 0
    if request.user == username:
        flag = 1

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user_id=user.id)
    return render(request, 'edit-profile-interests.html', {'flag':flag,'user':user,'profile':profile})

def edit_profile_work_edu(request,username):
    flag = 0
    if request.user == username:
        flag = 1

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user_id=user.id)
    return render(request, 'edit-profile-work-edu.html', {'flag':flag,'user':user,'profile':profile})

def edit_profile_password(request):
    return render(request, 'edit-profile-password.html')

def edit_profile_settings(request):
    return render(request, 'edit-profile-settings.html')

def contact(request):
    return render(request, 'contact.html')

def not_found(request):
    return render(request, '404.html')

def faq(request) :
    return render(request,'faq.html')

def newsfeed(request) :
    print(request.user)
    return render(request,'newsfeed.html')

def newsfeed_friends(request) :
    return render(request,'newsfeed-friends.html')

def newsfeed_images(request) :
    return render(request,'newsfeed-images.html')

def newsfeed_messages(request) :
    return render(request,'newsfeed-messages.html')

def newsfeed_people_nearby(request) :
    return render(request,'newsfeed-people-nearby.html')

def newsfeed_videos(request) :
    return render(request,'newsfeed-videos.html')
