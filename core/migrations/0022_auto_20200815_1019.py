# Generated by Django 3.0.8 on 2020-08-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20200815_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='img',
            field=models.ImageField(upload_to='items_img/'),
        ),
    ]
