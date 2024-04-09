from django.contrib import admin

# Register your models here.

from .models import Community, UserProfile

admin.site.register(Community)
admin.site.register(UserProfile)
