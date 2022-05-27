# Generated by Django 4.0.4 on 2022-05-22 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_App', '0013_history_restaurents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='product',
        ),
        migrations.RemoveField(
            model_name='history',
            name='restaurents',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='history',
            name='restaurent_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]