from django.contrib import admin
from .models import Community, PostTemplate, PostTemplateItem, Comment, Post
# Register your models here.

admin.site.register(Community)
admin.site.register(PostTemplate)
admin.site.register(PostTemplateItem)
admin.site.register(Comment)
admin.site.register(Post)
