# Generated by Django 5.0.4 on 2024-05-05 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0013_remove_comment_post_post_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='invites',
            new_name='requests',
        ),
    ]
