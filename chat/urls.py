from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('newsfeed-messages',views.newsfeed_messages, name='newsfeed_messages'),
  path('<str:room_name>/', views.room, name='room'),
]