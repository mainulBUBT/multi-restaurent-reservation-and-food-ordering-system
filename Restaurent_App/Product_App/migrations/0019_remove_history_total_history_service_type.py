# Generated by Django 4.0.4 on 2022-05-24 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_App', '0018_order_service_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='total',
        ),
        migrations.AddField(
            model_name='history',
            name='service_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
