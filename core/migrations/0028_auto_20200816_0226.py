# Generated by Django 3.0.8 on 2020-08-16 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20200816_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='dislikes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='posted_time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
