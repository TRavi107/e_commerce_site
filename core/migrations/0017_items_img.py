# Generated by Django 3.0.8 on 2020-08-15 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_order_billing_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
