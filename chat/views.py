from django.shortcuts import render
from typing import List
from django.contrib.auth.models import User, auth
from .models import Message
from friends.models import Profile
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
  return render(request, 'chat/index.html')

def newsfeed_messages(request) :
    if 'username' in request.session :
        user = User.objects.get(username = request.session["username"])
        profile = Profile.objects.get(user_id = user.id)
        friendlist = []
        friends = profile.friendlist 
        if friends is not None :
            for friend in friends :
                if friend is not None :
                    user = User.objects.get(username = friend)
                    profile = Profile.objects.get(user_id = user.id)
                    friendlist.append(profile)
        otheruser = Profile.objects.all()
        user = User.objects.get(username = request.session["username"])
        profile = Profile.objects.get(user_id = user.id)
        return render(request,'chat/newsfeed-messages.html', {'profile': friendlist, 'users':otheruser,'myuser':profile })
    messages.info(request, 'First you need to loging for view my-profile')
    return HttpResponseRedirect('/index-register' )  

def room(request, room_name):
  username = request.GET.get('username', 'Anonymous')
  # Get the messages from the database
  messages = Message.objects.filter(room=room_name)[0:25]

  return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages':messages})  
