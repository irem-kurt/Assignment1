from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    location = PlainLocationField(default='41.0255493,28.9742571', zoom=7, blank=False, null=False)
    picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    unreadcount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name}  {self.user.last_name}"
