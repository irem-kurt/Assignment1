# Generated by Django 5.0.4 on 2024-05-04 14:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0005_post_comments_post_communit_id_picturesection'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specializedpost',
            name='author',
        ),
        migrations.RemoveField(
            model_name='specializedpost',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='specializedpost',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='specializedpost',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='community',
            name='location',
        ),
        migrations.RemoveField(
            model_name='community',
            name='posts',
        ),
        migrations.AddField(
            model_name='comment',
            name='reported',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='community',
            name='invites',
            field=models.ManyToManyField(blank=True, related_name='invited_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='community',
            name='rules',
            field=models.TextField(default='First Rule of Community: you do not talk about the community.'),
        ),
        migrations.DeleteModel(
            name='PictureSection',
        ),
        migrations.DeleteModel(
            name='SpecializedPost',
        ),
    ]
