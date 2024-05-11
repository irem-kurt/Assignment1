from django.db import models
from django.dispatch import receiver
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    location = PlainLocationField(default='41.012791, 28.964593', zoom=7, blank=False, null=False)
    picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png')
    followers = models.ManyToManyField(User, blank=True, related_name='followers', symmetrical=False)
    unreadcount = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

