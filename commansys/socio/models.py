from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from location_field.models.plain import PlainLocationField
# Create your models here.


class Tag(models.Model):
    tag = models.TextField(default='', blank=False, null=False)
    requester = models.ForeignKey(User, verbose_name='user', related_name='requester', blank=True, null=True, on_delete=models.SET_NULL)
    toPerson = models.OneToOneField(User, verbose_name='user', related_name='toPerson', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.tag
    class Meta:
        app_label = 'socio' 

class Community(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #old creator
    managers = models.ManyToManyField(User, related_name='managed_communities')
    createdDate = models.DateTimeField(default=timezone.now)
    name = models.TextField(default="Community Name", max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/service_pictures/', default='uploads/service_pictures/default.png')
    #location = PlainLocationField(default='41.0255493,28.9742571', zoom=7, blank=False, null=False)
    #followers = models.ManyToManyField(User, related_name='followed_communities')
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    #category = models.ForeignKey(Tag, verbose_name='category', related_name='category', blank=True, null=True, on_delete=models.SET_NULL)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    #location = PlainLocationField(default='41.0255493,28.9742571', zoom=7, blank=False, null=False)
    picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    unreadcount = models.IntegerField(default=0)

class NotifyUser(models.Model):
    notify = models.ForeignKey(User, verbose_name='user', related_name='notify', on_delete=models.CASCADE)
    notification = models.TextField(blank=True, null=True)
    hasRead = models.BooleanField(default=False)
    offerType = models.TextField(blank=True, null=True)
    offerPk = models.IntegerField(default=0)


'''class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, related_name='followed_communities')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_communities')
    managers = models.ManyToManyField(User, related_name='managed_communities')

class PostTemplate(models.Model):
    name = models.CharField(max_length=255)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='templates')
    settings = models.JSONField()  # Assuming settings will be stored as JSON
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    input = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    template = models.ForeignKey(PostTemplate, on_delete=models.CASCADE)

class Comment(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
'''