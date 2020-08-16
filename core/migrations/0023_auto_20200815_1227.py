# Generated by Django 3.0.8 on 2020-08-15 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20200815_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='comments',
            field=models.ManyToManyField(to='core.Comments'),
        ),
    ]
