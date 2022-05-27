# Generated by Django 4.0.4 on 2022-05-24 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product_App', '0015_history_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.AddField(
            model_name='history',
            name='order_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='price',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='product_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='quantity',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='restaurent_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='total',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='restaurents',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Product_App.restaurent'),
        ),
    ]
