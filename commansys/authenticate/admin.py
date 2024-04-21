from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Register your models here.

admin.site.unregister(Group)
admin.site.register(Profile)


'''class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
'''
