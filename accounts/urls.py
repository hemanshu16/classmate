from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
   path('index-register', views.index_register, name='index_register'),
   path('login', views.login, name='login'),
   path('forgotpassword', views.password_reset, name="password_reset"),
   path('password-change', views.password_change, name="password_change")
]