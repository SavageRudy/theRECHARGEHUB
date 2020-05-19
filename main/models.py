from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    num = models.CharField(max_length=20)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Combo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    net = models.CharField(max_length=40)
    talk = models.CharField(max_length=40)
    vald = models.CharField(max_length=40)
    price = models.IntegerField()   
    text = models.TextField()
    def __str__(self):
        return f" A  {self.name} plan with  {self.talk}rs talkitime,{self.net} data package and validity of {self.vald} days"

class Internet(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    net = models.CharField(max_length=40)
    vald = models.CharField(max_length=40)
    price = models.IntegerField()   
    text = models.TextField()
    def __str__(self):
        return f" A  {self.name} plan with  {self.net} data package and validity of {self.vald} days"

class Talktime(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    talk = models.CharField(max_length=40)
    vald = models.CharField(max_length=40)
    price = models.IntegerField()   
    text = models.TextField()   
    def __str__(self):
        return f" A  {self.name} plan with  {self.talk}rs talkitime and validity of {self.vald} days"

