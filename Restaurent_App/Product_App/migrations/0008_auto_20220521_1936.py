# Generated by Django 3.2 on 2022-05-21 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_App', '0007_auto_20220521_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurent',
            name='restaurent_pics',
            field=models.ImageField(blank=True, upload_to='restaurent_pics'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='person',
            field=models.IntegerField(default='1'),
        ),
    ]