# Generated by Django 4.0.4 on 2022-05-22 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product_App', '0009_order_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total',
            new_name='price',
        ),
    ]
