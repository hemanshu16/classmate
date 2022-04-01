from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Message(models.Model):
  username = models.CharField(max_length=255)
  room = models.CharField(max_length=255)
  currentUser = models.CharField(max_length=255,null=True)
  content = models.TextField()
  date_added = models.TextField()

  class Meta:
    ordering = ('id',)
