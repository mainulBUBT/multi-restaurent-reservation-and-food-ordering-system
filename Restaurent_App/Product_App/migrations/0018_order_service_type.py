# Generated by Django 4.0.4 on 2022-05-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_App', '0017_history_product_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='service_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
