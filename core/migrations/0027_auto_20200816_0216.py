# Generated by Django 3.0.8 on 2020-08-16 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200816_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Items'),
        ),
    ]
