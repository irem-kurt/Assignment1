# Generated by Django 4.2.1 on 2024-04-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='category',
        ),
        migrations.AlterField(
            model_name='community',
            name='location',
            field=models.CharField(default='41.0255493,28.9742571,7', max_length=50),
        ),
    ]
