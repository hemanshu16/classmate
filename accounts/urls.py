from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
   path('index-register', views.index_register, name='index_register')
]