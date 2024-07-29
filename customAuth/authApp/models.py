from django.db import models

# Create your models here.

class MyUser(models.Model):
 name = models.CharField(max_length=255)
 email = models.EmailField(max_length=500, unique=True)
 username = models.CharField(max_length=255, unique=True)
 password = models.CharField(max_length=255)
 
class Stickies(models.Model):
  creatorId= models.CharField(max_length=255)
  sticky= models.CharField(max_length=500)
  created_at= models.DateTimeField(auto_now_add=True)


def __str__(self):
  return self.username