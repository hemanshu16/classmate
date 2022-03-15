from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('edit-profile-basic', views.edit_profile_basic, name='edit_profile_basic'),
    path('edit-profile-interests', views.edit_profile_interests, name='edit_profile_interests'),
    path('edit-profile-password', views.edit_profile_password, name='edit_profile_password'),
    path('edit-profile-work-edu', views.edit_profile_work_edu, name='edit_profile_work_edu'),
    path('edit-profile-settings', views.edit_profile_settings, name='edit_profile_settings'),
    path('contact', views.contact, name='contact'),
    path('404', views.not_found, name='not_found'),
    path('faq', views.faq, name='faq'),
    path('newsfeed',views.newsfeed, name='newsfeed'),
    path('',views.newsfeed, name='newsfeed'),
    path('newsfeed-friends',views.newsfeed_friends, name='newsfeed_friends'),
    path('newsfeed-images',views.newsfeed_images, name='newsfeed_images'),
    path('newsfeed-messages',views.newsfeed_messages, name='newsfeed_messages'),
    path('newsfeed-people-nearby',views.newsfeed_people_nearby, name='newsfeed_people_nearby'),
    path('newsfeed-videos', views.newsfeed_videos, name='newsfeed_videos'),
    path('update-interest', views.update_interest, name="update_intereset"),
    path('update-education-details', views.update_education_details, name="update_edutcation_details")
]