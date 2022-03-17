from typing import List
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
import friends
from friends.models import Profile
from friends.models import Post
from friends.models import Comment
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime
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

            if 'profileimg' in request.FILES:
               profile.image = request.FILES["profileimg"] 
            user.save()   
            profile.save()
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

            if "submitlike" in request.POST:
               print(request.POST["postid"])
               post_for_like = Post.objects.get(id=int(request.POST["postid"]))
               print(post_for_like.likedby)
               if post_for_like.likedby is None:
                   post_for_like.likes = post_for_like.likes + 1
                   List1 = [request.session['username']]
                   post_for_like.likedby = List1
                   post_for_like.save()
               elif request.session['username'] not in post_for_like.likedby:
                   post_for_like.likes = post_for_like.likes + 1
                   if post_for_like.likedby is not None :
                      post_for_like.likedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_like.likedby = List1
                   post_for_like.save()   

            if "submitdislike" in request.POST:
               post_for_dislike = Post.objects.get(id= int(request.POST["postid"]))
               if post_for_dislike.dislikedby is None:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   List1 = [request.session['username']]
                   post_for_dislike.dislikedby = List1
                   post_for_dislike.save()
               elif request.session['username'] not in post_for_dislike.dislikedby:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   if post_for_dislike.dislikedby is not None :
                      post_for_dislike.dislikedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_dislike.dislikedby = List1
                   post_for_dislike.save() 

            if "submitcomment" in request.POST:
                comment = Comment(post_id=int(request.POST["postid"]),comment=request.POST["comment"],username=request.session["username"])
                comment.save()

        post = Post.objects.filter().order_by('-id')
        comment = Comment.objects.all()
        otheruser = Profile.objects.all()
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
        otheruser = Profile.objects.all()
        user = User.objects.get(username = request.session["username"])
        profile = Profile.objects.get(user_id = user.id)
        return render(request,'newsfeed-friends.html', {'profile': friendlist, 'users':otheruser,'myuser':profile })
    messages.info(request, 'First you need to loging for view my-profile')
    return HttpResponseRedirect('/index-register' )    

def timeline_about(request,username = None) :
    
    if username is  None :
        if 'username' in request.session : 
            username = request.session['username']
        else :
            messages.info(request, 'First you need to loging for view my-profile')
            return HttpResponseRedirect('/index-register' )
    if(User.objects.filter(username = username).exists()):
       user = User.objects.get(username = username)
       profile = Profile.objects.get(user_id = user.id)
       return render(request, "timeline-about.html", {'profile' : profile})
    return render(request,"404.html")

def timeline(request,username = None) :
    
    if username is  None :
        if 'username' in request.session : 
            username = request.session['username']
        else :
            messages.info(request, 'First you need to loging for view my-profile')
            return HttpResponseRedirect('/index-register' )
    if(User.objects.filter(username = username).exists()):
       user = User.objects.get(username = username)
       profile = Profile.objects.get(user_id = user.id)

       if request.method == "POST":
           if "submitlike" in request.POST:
               print(request.POST["postid"])
               post_for_like = Post.objects.get(id=int(request.POST["postid"]))
               print(post_for_like.likedby)
               if post_for_like.likedby is None:
                   post_for_like.likes = post_for_like.likes + 1
                   List1 = [request.session['username']]
                   post_for_like.likedby = List1
                   post_for_like.save()
               elif request.session['username'] not in post_for_like.likedby:
                   post_for_like.likes = post_for_like.likes + 1
                   if post_for_like.likedby is not None :
                      post_for_like.likedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_like.likedby = List1
                   post_for_like.save()   

           if "submitdislike" in request.POST:
               post_for_dislike = Post.objects.get(id= int(request.POST["postid"]))
               if post_for_dislike.dislikedby is None:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   List1 = [request.session['username']]
                   post_for_dislike.dislikedby = List1
                   post_for_dislike.save()
               elif request.session['username'] not in post_for_dislike.dislikedby:
                   post_for_dislike.dislikes = post_for_dislike.dislikes + 1
                   if post_for_dislike.dislikedby is not None :
                      post_for_dislike.dislikedby.append(request.session['username'])
                   else : 
                      List1 = [request.session['username']]
                      post_for_dislike.dislikedby = List1
                   post_for_dislike.save() 

           if "submitcomment" in request.POST:
                comment = Comment(post_id=int(request.POST["postid"]),comment=request.POST["comment"],username=request.session["username"])
                comment.save()
       post = Post.objects.filter(username=username)
       comments = Comment.objects.filter()
       return render(request, "timeline.html", {'profile' : profile,'posts':post,'comments':comments})
    return render(request,"404.html")

def newsfeed_images(request) :
    return render(request,'newsfeed-images.html')

def newsfeed_messages(request) :
    return render(request,'newsfeed-messages.html')

def newsfeed_people_nearby(request) :
     if 'username' in request.session :
        user = User.objects.get(username=request.session["username"])
        profile = Profile.objects.get(user_id=user.id)
        otheruser = Profile.objects.all()
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
            profile.friendlist.append(friend)
        else : 
           print(friend)
           List1 = [friend]
           profile.friendlist = List1
        profile.save()
        return HttpResponseRedirect('/newsfeed-friends' )
    messages.info(request, 'First you need to loging for view my-profile')
    return HttpResponseRedirect('/index-register' )


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index-register' )
