from typing import List
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
import friends
import os
from chat.models import Message
from friends.models import Profile
from friends.models import Post
from friends.models import Comment
from friends.models import RememberList
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import datetime

from django.conf import settings
# Create your views here.

def index(request) :
    return render(request,'index.html')

# def index_register(request):
#    return render(request, 'index-register.html')


def edit_profile_basic(request):
    print("hello")
    if 'username' in request.session :
        username = request.session["username"]
        if(request.method == "POST") :
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            email = request.POST['email']
            day = request.POST["date"]
            month = request.POST["month"]
            year = request.POST["year"]
            gender = request.POST["gender"]
            city = request.POST["city"]
            country = request.POST["country"]
            information = request.POST["information"]
            user = User.objects.get(username = username)
            profile = Profile.objects.get(user_id=user.id)
            user.first_name = firstname
            user.last_name = lastname
            profile.user.first_name = firstname
            profile.user.last_name = lastname
            if(user.email != email and User.objects.filter(email = email).exists()):
                messages.info(request, str(email) + 'This email is already exists')
            else : 
                profile.user.email = email
                user.email = email
            profile.dateOfBirth = datetime.datetime(int(year), int(month), int(day))
            profile.city = city
            profile.country = country
            profile.aboutMe = information
            profile.gender = gender
            if request.FILES["banner-image"] is not None :
                profile.banner_image = request.FILES["banner-image"]
            if 'profileimg' in request.FILES:
               if(os.path.exists(os.path.join('C:/Users/Visha/Documents/GitHub/ClassMate/media/',str(profile.image.name)))) :
                  os.remove(os.path.join('C:/Users/Visha/Documents/GitHub/ClassMate/media/',str(profile.image.name))) 
               profile.image = request.FILES["profileimg"] 
            user.save()   
            profile.save()
            messages.info(request,"Successfully Updated . . .")
        user1 = User.objects.get(username=request.session["username"])
        profile1 = Profile.objects.get(user_id=user1.id)
        return render(request, "edit-profile-basic.html",{'user':user1,'profile':profile1})
    else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )

def edit_profile_interests(request):
    
    if 'username' in request.session :
        user = User.objects.get(username=request.session["username"])
        profile = Profile.objects.get(user_id=user.id)
        return render(request, 'edit-profile-interests.html', {'user':user,'profile':profile})
    else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )
    

def update_interest(request) :
    if 'username' in request.session :
        username = request.session["username"]
        user = User.objects.get(username = username)
        profile = Profile.objects.get(user_id = user.id)
        profile.interestDesc = request.POST["interestdesc"]
        interest = request.POST['interest'].strip()
        if profile.interestList is not None :
            if len(interest) > 0 :
                profile.interestList.append(request.POST['interest'])
        elif  len(interest) > 0 : 
           List1 = [request.POST['interest']]
           profile.interestList = List1
        profile.save()
        messages.info(request,"Successfully Updated...")
        return HttpResponseRedirect('/edit-profile-interests')
    else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )

def edit_profile_work_edu(request):

    if 'username' in request.session :
        user = User.objects.get(username=request.session["username"])
        profile = Profile.objects.get(user_id=user.id)
        return render(request, 'edit-profile-work-edu.html', {'user':user,'profile':profile})
    else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )

def update_education_details(request) :
    user  = User.objects.get(username = request.session["username"])
    profile = Profile.objects.get(user_id = user.id)
    profile.universityName = request.POST["school"]
    profile.startYear = int(request.POST["start"])
    profile.endYear = int(request.POST["end"])
    profile.educationDesc = request.POST["description"]
    profile.save()
    messages.info(request,"Successfully Updated. . .")
    return HttpResponseRedirect('/edit-profile-work-edu')

  
def edit_profile_password(request):
    if 'username' in request.session :
        username = request.session["username"]
        if request.method == "POST" :
            user = User.objects.get(username = request.session["username"])
            if(user.check_password(request.POST["oldpassword"])) :
                if ( request.POST["newpassword"] == request.POST["newcpassword"]) :
                    user.set_password(request.POST["newpassword"])
                    messages.info(request, 'Your Password is reset to New Password')
                    user.save()
                else : 
                    messages.info(request, 'Password and Confirm Password must be same')
            else :
                messages.info(request, 'Old password is Wrong')
        
        user1 = User.objects.get(username=request.session["username"])
        profile1 = Profile.objects.get(user_id=user1.id)
        return render(request,'edit-profile-password.html', {'user':user1,'profile':profile1})
    else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )

def edit_profile_settings(request):
    return render(request, 'edit-profile-settings.html')

def contact(request):
    return render(request, 'contact.html')

def remember_list(request):

    if "updateRemember" in request.POST:
        username = request.session["username"]
        friend = request.POST["friend"]
        memory = RememberList.objects.get(username = username,friend = friend)
        memory.username = username
        memory.friend = friend
        memory.desc = request.POST["desc"]
        memory.save()
        messages.info(request,"Successfully Updated...")

    if "deleteremember" in request.POST :
        RememberList.objects.filter(id=int(request.POST['deleteremember'])).delete()
        messages.info(request,"Successfully Deleted...")    
    remember = RememberList.objects.filter(username = request.session["username"])
    user = User.objects.get(username=request.session["username"])
    profile = Profile.objects.get(user_id=user.id)
    return render(request, 'remember-list.html', {'rememberList':remember,'user':user,'profile':profile})    

def not_found(request):
    return render(request, '404.html')

def faq(request) :
    return render(request,'faq.html')

def newsfeed(request) :
    if 'username' in request.session :
        user = User.objects.get(username=request.session["username"])
        profile = Profile.objects.get(user_id=user.id)

        if request.method == "POST":

            if "submitpost" in request.POST:
               post = Post(username=request.session["username"],image=request.FILES["postImg"],desc=request.POST["desc"],likes=0,dislikes=0,postdate=datetime.date.today())
               post.save()
               messages.info(request,"Congrats. . . for a new Post")

            if "submitlike" in request.POST:
               print(request.POST["postid"])
               post_for_like = Post.objects.get(id=int(request.POST["postid"]))
               print(post_for_like.likedby)
               if post_for_like.likedby is None:
                    post_for_like.likes = post_for_like.likes + 1
                    List1 = [request.session['username']]
                    post_for_like.likedby = List1

                    if post_for_like.dislikedby is not None and request.session['username'] in post_for_like.dislikedby :
                        post_for_like.dislikes = post_for_like.dislikes - 1
                        post_for_like.dislikedby.remove(request.session['username'])
                    post_for_like.save()
               elif request.session['username'] not in post_for_like.likedby:
                   post_for_like.likes = post_for_like.likes + 1
                   if post_for_like.likedby is not None :
                      post_for_like.likedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_like.likedby = List1
                   if post_for_like.dislikedby is not None and request.session['username'] in post_for_like.dislikedby :
                        post_for_like.dislikes = post_for_like.dislikes - 1
                        post_for_like.dislikedby.remove(request.session['username'])   
                   post_for_like.save()   

            if "submitdislike" in request.POST:
               post_for_dislike = Post.objects.get(id= int(request.POST["postid"]))
               if post_for_dislike.dislikedby is None:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   List1 = [request.session['username']]
                   post_for_dislike.dislikedby = List1
                   if post_for_dislike.likedby is not None and request.session['username'] in post_for_dislike.likedby :
                        post_for_dislike.likes = post_for_dislike.likes - 1
                        post_for_dislike.likedby.remove(request.session['username'])
                   post_for_dislike.save()
               elif request.session['username'] not in post_for_dislike.dislikedby:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   if post_for_dislike.dislikedby is not None :
                      post_for_dislike.dislikedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_dislike.dislikedby = List1
                   if post_for_dislike.likedby is not None and request.session['username'] in post_for_dislike.likedby :
                        post_for_dislike.likes = post_for_dislike.likes - 1
                        post_for_dislike.likedby.remove(request.session['username'])
                   post_for_dislike.save()
                  

            if "submitcomment" in request.POST:
                comment = Comment(post_id=int(request.POST["postid"]),comment=request.POST["comment"],username=request.session["username"])
                comment.save()
                messages.info(request,"Comment Saved. . .")

         
            if "deletecomment" in request.POST :
                Comment.objects.filter(id=int(request.POST['commentid'])).delete()
                messages.info(request,"Comment Deleted")
            
        post = Post.objects.filter().order_by('-id')
        comment = Comment.objects.all()
        otheruser = Profile.objects.filter(universityName=profile.universityName)
        otheruser = otheruser.exclude(id = profile.id)
        friendlist = []
        friends = profile.friendlist 
        if friends is not None :
            for friend in friends :
                if friend is not None :
                    user = User.objects.get(username = friend)
                    friendlist.append(user)
        for user in friendlist :
            otheruser = otheruser.exclude(user_id = user.id)
        return render(request, 'newsfeed.html', {'profile':profile,'otherusers':otheruser,'posts':post,'comments':comment})
    else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )


def newsfeed_friends(request) :
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
        user = User.objects.get(username = request.session["username"])
        profile = Profile.objects.get(user_id = user.id)
        otheruser = Profile.objects.filter(universityName=profile.universityName)
        return render(request,'newsfeed-friends.html', {'profile': friendlist, 'users':otheruser,'myuser':profile })
    messages.info(request, 'First you need to loging for view my-profile')
    return HttpResponseRedirect('/index-register' )    

def timeline_about(request,username = None) :
    flag = 0
    if username is  None :
        if 'username' in request.session : 
            flag = 1
            username = request.session['username']
        else :
            messages.info(request, 'First you need to loging for view my-profile')
            return HttpResponseRedirect('/index-register' )
    if(User.objects.filter(username = username).exists()):
       user = User.objects.get(username = username)
       profile = Profile.objects.get(user_id = user.id)
       remember = RememberList.objects.filter(username = request.session["username"])
       return render(request, "timeline-about.html", {'profile' : profile,'flag':flag,'rememberList':remember})
    return render(request,"404.html")
 

def timeline(request,username = None) :
    flag = 0
    if username is  None :
        if 'username' in request.session : 
            flag = 1
            username = request.session['username']
        else :
            messages.info(request, 'First you need to loging for view my-profile')
            return HttpResponseRedirect('/index-register' )
    if(User.objects.filter(username = username).exists()):
       user = User.objects.get(username = username)
       profile = Profile.objects.get(user_id = user.id)

       if "submitRemember" in request.POST:
           
           try:
              remember = RememberList.objects.get(username=request.session["username"],friend=username)
           except RememberList.DoesNotExist:
              remember = None

           if remember is None:
               memory = RememberList(username=request.session["username"],friend=username,desc=request.POST["desc"])
               memory.save()
               messages.info(request,"Successfully Saved. . .")
           else:
               remember.username = request.session["username"]
               remember.friend = username
               remember.desc = request.POST["desc"]
               remember.save()
               messages.info(request,"Successfully Updated. . .")

       
       if "submitpost" in request.POST:
               post = Post(username=request.session["username"],image=request.FILES["postImg"],desc=request.POST["desc"],likes=0,dislikes=0,postdate=datetime.date.today())
               post.save()
               messages.info(request,"Successfully Saved. . .")

       if request.method == "POST":
           if "submitlike" in request.POST:
               print(request.POST["postid"])
               post_for_like = Post.objects.get(id=int(request.POST["postid"]))
               print(post_for_like.likedby)
               if post_for_like.likedby is None:
                   post_for_like.likes = post_for_like.likes + 1
                   List1 = [request.session['username']]
                   post_for_like.likedby = List1
                   if post_for_like.dislikedby is not None and request.session['username'] in post_for_like.dislikedby :
                        post_for_like.dislikes = post_for_like.dislikes - 1
                        post_for_like.dislikedby.remove(request.session['username'])
                   post_for_like.save()
               elif request.session['username'] not in post_for_like.likedby:
                   post_for_like.likes = post_for_like.likes + 1
                   if post_for_like.likedby is not None :
                      post_for_like.likedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_like.likedby = List1
                   if post_for_like.dislikedby is not None and request.session['username'] in post_for_like.dislikedby :
                        post_for_like.dislikes = post_for_like.dislikes - 1
                        post_for_like.dislikedby.remove(request.session['username'])   
                   post_for_like.save()   

           if "submitdislike" in request.POST:
               post_for_dislike = Post.objects.get(id= int(request.POST["postid"]))
               if post_for_dislike.dislikedby is None:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   List1 = [request.session['username']]
                   post_for_dislike.dislikedby = List1
                   if post_for_dislike.likedby is not None and request.session['username'] in post_for_dislike.likedby :
                        post_for_dislike.likes = post_for_dislike.likes - 1
                        post_for_dislike.likedby.remove(request.session['username'])
                   post_for_dislike.save()
               elif request.session['username'] not in post_for_dislike.dislikedby:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   if post_for_dislike.dislikedby is not None :
                      post_for_dislike.dislikedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_dislike.dislikedby = List1
                   if post_for_dislike.likedby is not None and request.session['username'] in post_for_dislike.likedby :
                        post_for_dislike.likes = post_for_dislike.likes - 1
                        post_for_dislike.likedby.remove(request.session['username'])
                   post_for_dislike.save()

           if "submitcomment" in request.POST:
                if len(request.POST["comment"].strip()) > 0 :
                    comment = Comment(post_id=int(request.POST["postid"]),comment=request.POST["comment"],username=request.session["username"])
                    comment.save()
                    messages.info(request,"Successfully Saved. . .")

           if "deletepost" in request.POST :
               Post.objects.filter(id=int(request.POST['deletepost'])).delete()
               messages.info(request,"Successfully Deleted. . .")

           if "deletecomment" in request.POST :
                Comment.objects.filter(id=int(request.POST['commentid'])).delete()
                messages.info(request,"Successfully Deleted. . .")   

       post = Post.objects.filter(username=username)
       comments = Comment.objects.filter()
       user = User.objects.get(username=request.session["username"])
       loggedUser = Profile.objects.get(user_id=user.id)
       return render(request, "timeline.html", {'profile' : profile,'loggedUser':loggedUser ,'posts':post,'comments':comments,'flag':flag})
    return render(request,"404.html")

def newsfeed_images(request) :
     if 'username' in request.session :
        user = User.objects.get(username=request.session["username"])
        profile = Profile.objects.get(user_id=user.id)

        if request.method == "POST":

            if "submitpost" in request.POST:
               post = Post(username=request.session["username"],image=request.FILES["postImg"],desc=request.POST["desc"],likes=0,dislikes=0,postdate=datetime.date.today())
               post.save()
               messages.info(request,"Successfully Saved. . .")

            if "submitlike" in request.POST:
               print(request.POST["postid"])
               post_for_like = Post.objects.get(id=int(request.POST["postid"]))
               print(post_for_like.likedby)
               if post_for_like.likedby is None:
                    post_for_like.likes = post_for_like.likes + 1
                    List1 = [request.session['username']]
                    post_for_like.likedby = List1

                    if post_for_like.dislikedby is not None and request.session['username'] in post_for_like.dislikedby :
                        post_for_like.dislikes = post_for_like.dislikes - 1
                        post_for_like.dislikedby.remove(request.session['username'])
                    post_for_like.save()
               elif request.session['username'] not in post_for_like.likedby:
                   post_for_like.likes = post_for_like.likes + 1
                   if post_for_like.likedby is not None :
                      post_for_like.likedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_like.likedby = List1
                   if post_for_like.dislikedby is not None and request.session['username'] in post_for_like.dislikedby :
                        post_for_like.dislikes = post_for_like.dislikes - 1
                        post_for_like.dislikedby.remove(request.session['username'])   
                   post_for_like.save()   

            if "submitdislike" in request.POST:
               post_for_dislike = Post.objects.get(id= int(request.POST["postid"]))
               if post_for_dislike.dislikedby is None:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   List1 = [request.session['username']]
                   post_for_dislike.dislikedby = List1
                   if post_for_dislike.likedby is not None and request.session['username'] in post_for_dislike.likedby :
                        post_for_dislike.likes = post_for_dislike.likes - 1
                        post_for_dislike.likedby.remove(request.session['username'])
                   post_for_dislike.save()
               elif request.session['username'] not in post_for_dislike.dislikedby:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   if post_for_dislike.dislikedby is not None :
                      post_for_dislike.dislikedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_dislike.dislikedby = List1
                   if post_for_dislike.likedby is not None and request.session['username'] in post_for_dislike.likedby :
                        post_for_dislike.likes = post_for_dislike.likes - 1
                        post_for_dislike.likedby.remove(request.session['username'])
                   post_for_dislike.save()
                  

            if "submitcomment" in request.POST:
                comment = Comment(post_id=int(request.POST["postid"]),comment=request.POST["comment"],username=request.session["username"])
                comment.save()
                messages.info(request,"Successfully Saved. . .")
         
            if "deletecomment" in request.POST :
                Comment.objects.filter(id=int(request.POST['commentid'])).delete()
                messages.info(request,"Successfully Delete. . .")
            
        post = Post.objects.filter().order_by('-likes').order_by('dislikes')
        comment = Comment.objects.all()
        otheruser = Profile.objects.filter(universityName=profile.universityName)
        return render(request, 'newsfeed-images.html', {'profile':profile,'otherusers':otheruser,'posts':post,'comments':comment})
     else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )

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
        chatlist = []
        roomname = ""
        if friend is not None :
            for friend in friends :
                if friend is not None :
                    friend_obj = User.objects.get(username = friend)
                    friend_id = friend_obj.id
                    if(friend_id > user.id) :
                        roomname = friend + user.username
                    else :
                        roomname = user.username + friend
                    chats = []
                    chats = Message.objects.filter(room = roomname)
                    chatlist.append(chats)
        return render(request,'newsfeed-messages.html', {'profile': friendlist, 'users':otheruser,'myuser':profile,'chatlist':chatlist })
    messages.info(request, 'First you need to loging for view my-profile')
    return HttpResponseRedirect('/index-register' )

def newsfeed_people_nearby(request) :
     if 'username' in request.session :
        user = User.objects.get(username=request.session["username"])
        profile = Profile.objects.get(user_id=user.id)
        otheruser = Profile.objects.filter(universityName=profile.universityName)
        return render(request, 'newsfeed-people-nearby.html', {'profile':profile,'otherusers':otheruser})
     else :
        messages.info(request, "First You have to Login")
        return HttpResponseRedirect('/index-register' )

def newsfeed_videos(request) :
    return render(request,'newsfeed-videos.html')

def add_friend(request,friend) :
    if "username" in request.session :
        user = User.objects.get(username = request.session["username"])
        profile = Profile.objects.get(user_id= user.id)
        if profile.friendlist is not None :
            if friend  not in profile.friendlist :
                profile.friendlist.append(friend)
        else : 
           print(friend)
           List1 = [friend]
           profile.friendlist = List1
        profile.save()
        messages.info(request,"Successfully Saved. . .")
        return HttpResponseRedirect('/newsfeed-friends' )
    messages.info(request, 'First you need to loging for view my-profile')
    return HttpResponseRedirect('/index-register' )


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index-register' )

def contact_mail(request):
    subject = 'Contact Information'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['info.classmate.official@gmail.com']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    messag = request.POST['message']
    message =  "    User name : " + name + "\n"
    message += "    User Email : " + email + "\n"
    message += "    user Phone No :" + phone + "\n"
    message += "    User Message : " + messag
    send_mail( subject, message, email_from, recipient_list )
    messages.info(request,"Message is Successfully send.")
    return render(request,'contact.html')