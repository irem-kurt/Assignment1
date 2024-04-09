from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
#from location_field.models.plain import PlainLocationField

class Community(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    name = models.TextField(default="Community Name", blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/community_pictures/', default='uploads/community_pictures/default.png')
    #location = PlainLocationField(default='41.0255493,28.9742571', zoom=7, blank=False, null=False)
    #category = models.ForeignKey(Tag, verbose_name='category', related_name='category', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    #location = PlainLocationField(default='41.0255493,28.9742571', zoom=7, blank=False, null=False)
    picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
