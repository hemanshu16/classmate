from statistics import mode
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

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
    image = models.ImageField(upload_to='pics', null=True)