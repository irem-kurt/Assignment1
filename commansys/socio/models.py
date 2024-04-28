from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from location_field.models.plain import PlainLocationField
from django.urls import reverse
from django.utils.text import slugify
from authenticate.models import Profile

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

    posts = models.ManyToManyField('Post', related_name='communities')

    class Meta:
        app_label = 'socio' 


class Post(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    content = models.TextField()
    link = models.CharField(max_length=500, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Changed to User
    slug = models.SlugField(default="", null=False, blank=True, db_index=True)
    likers = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikers = models.ManyToManyField(User, related_name='disliked_posts', blank=True)  # Added dislikers field
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("postDetailUrl", args=[self.slug])

    def __str__(self):
        return f"{self.title}  {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    text = models.TextField()

