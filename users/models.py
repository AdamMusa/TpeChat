from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)

    def __str__(self):
        return "{} Profile".format(self.user.username)

    
def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)
