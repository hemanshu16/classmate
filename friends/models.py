from statistics import mode
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

import friends

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateOfBirth = models.DateField(null=True)
    gender = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    country = models.CharField(max_length=100,null=True)
    aboutMe = models.TextField(null=True)
    universityName = models.CharField(max_length=100,null=True)
    startYear = models.IntegerField(null=True)
    endYear = models.IntegerField(null=True)
    educationDesc = models.TextField(null=True)
    interestDesc = models.TextField(null=True)
    interestList = ArrayField(
            models.CharField(max_length=100, blank=True),
            size=20,null=True,
        )
    friendlist = ArrayField(
            models.CharField(max_length=100, blank=True),
            size=20,null=True,
        )
    image = models.ImageField(upload_to='pics', null=True)
    banner_image = models.ImageField(upload_to='pics', null=True)

class Post(models.Model):
    image = models.ImageField(upload_to='pics', null=True)
    desc = models.TextField(null = True)
    username = models.TextField(null = True)
    likes = models.IntegerField(default=0)
    likedby = ArrayField(
            models.CharField(max_length=100, blank=True),
            size=20,null=True,
        )
    dislikes = models.IntegerField(default=0)
    dislikedby = ArrayField(
            models.CharField(max_length=100, blank=True),
            size=20,null=True,
        ) 
    postdate = models.DateField(null=True)

class Comment(models.Model):
    username = models.TextField(null = True)
    comment = models.TextField(null = True)
    post_id = models.BigIntegerField(null = True)
