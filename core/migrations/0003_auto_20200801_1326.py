# Generated by Django 3.0.8 on 2020-08-01 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('categories', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1)),
                ('price', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
