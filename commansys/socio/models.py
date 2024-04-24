from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from location_field.models.plain import PlainLocationField

# Create your models here.




class Community(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #old creator
    managers = models.ManyToManyField(User, related_name='managed_communities')
    createdDate = models.DateTimeField(default=timezone.now)
    name = models.TextField(default="Community Name", max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/service_pictures/', default='uploads/service_pictures/default.png')
    #location = PlainLocationField(default='41.0255493,28.9742571', zoom=7, blank=False, null=False)
    location = models.CharField(default='410255493', max_length=150)
    followers = models.ManyToManyField(User, related_name='followed_communities')
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        app_label = 'socio' 


class NotifyUser(models.Model):
    notify = models.ForeignKey(User, verbose_name='user', related_name='notify', on_delete=models.CASCADE)
    notification = models.TextField(blank=True, null=True)
    hasRead = models.BooleanField(default=False)
    offerType = models.TextField(blank=True, null=True)
    offerPk = models.IntegerField(default=0)


'''class PostTemplate(models.Model):
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