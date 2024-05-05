from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from location_field.models.plain import PlainLocationField
from django.urls import reverse
from django.utils.text import slugify
from authenticate.models import Profile
from enum import Enum
import secrets
import string

class Community(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    managers = models.ManyToManyField(User, related_name='managed_communities')
    followers = models.ManyToManyField(User, related_name='followed_communities')
    createdDate = models.DateTimeField(default=timezone.now)
    name = models.TextField(default="Community Name", max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    rules = models.TextField(blank=False, null=False, default='First Rule of Community: you do not talk about the community.')
    picture = models.ImageField(upload_to='uploads/service_pictures/', default='uploads/service_pictures/default.png')
    #location = PlainLocationField(default='41.0255493,28.9742571', zoom=7, blank=False, null=False)
    location = models.CharField(default='410255493', max_length=150)
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    requests = models.ManyToManyField(User, related_name='invited_users', blank=True)

    class Meta:
        app_label = 'socio' 
    
class PostTemplateItemType(Enum):
    IMAGE = 'image'
    TEXT = 'text'
    VIDEO = 'video'
    AUDIO = 'audio'
    DATETIME = 'datetime'
    LOCATION = 'location'
       
    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]

class PostTemplateItem(models.Model):
    name = models.CharField(max_length=100, null=True)
    post_type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in PostTemplateItemType])
    mandatory = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/post_pictures/', null=True, blank=True)
    video = models.FileField(upload_to='uploads/post_video/', null=True, blank=True)
    audio = models.FileField(upload_to='uploads/post_audio/', null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)

class PostTemplate(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    fields = models.ManyToManyField(PostTemplateItem, related_name='post_templates') #Hangi form itemleri olduğunu tutuyor gerçek değerleri yok
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=False)
    
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    reported = models.BooleanField(default=False)
    
    
class Post(models.Model):
    template = models.ForeignKey(PostTemplate, on_delete=models.CASCADE, null=True, blank=True)
    fields = models.ManyToManyField(PostTemplateItem, related_name='posts') #Hangi form itemleri olduğunu gerçek değerleriyle tutuyor
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(default="", null=False, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True) # likes
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True) # dislikes
    comments = models.ManyToManyField(Comment, related_name='posts', blank=True) # comments
    communit_id = models.ForeignKey(Community, on_delete=models.CASCADE, null=True)
    reported = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("postDetailUrl", args=[self.slug])

    def __str__(self):
        return f"{self.slug}  {self.author}"

    def save(self, *args, **kwargs):
        alphabet = string.ascii_letters + string.digits
        self.slug = slugify(''.join(secrets.choice(alphabet) for i in range(16)))
        super().save(*args, **kwargs)
        
class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    invite = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    


    '''
    PostTempalteInstance
    name = 'Karşılaştırma Postu'
    fields = [PostTemplateItem(name = 'Before', post_type = 'image', mandatory = True),
        PostTemplateItem(name = 'After', post_type = 'image', mandatory = True),
        PostTemplateItem(name = 'Description', post_type = 'text', mandatory = False),]

    PostInstance    
    template = 2
    fields = [PostTemplateItem(name = 'Before', post_type = 'image', mandatory = True, image = 'uploads/1.jpg'),
        PostTemplateItem(name = 'After', post_type = 'image', mandatory = True, image = 'uploads/2.jpg'),
        PostTemplateItem(name = 'Description', post_type = 'text', mandatory = False, text = '2 sene önceki ameliyatım ve bugün'),]
    author = 9
    slug = 'sdfasdfakfnjb3944982u1'
    creat
    likes = [1, 5, 234, 45]
    dislike = [3]
    '''