from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Register your models here.

admin.site.unregister(Group)


'''class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
'''


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('picture_preview',)  # Add this line to display picture preview

    def picture_preview(self, obj):
        return obj.picture.url if obj.picture else None

    picture_preview.short_description = 'Profile Picture'  # Customize the column header

# Register the Profile model with the custom admin class
admin.site.register(Profile, ProfileAdmin)