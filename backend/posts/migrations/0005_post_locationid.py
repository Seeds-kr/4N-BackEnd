# Generated by Django 4.2.3 on 2023-11-14 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_post_image_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='locationid',
            field=models.TextField(default=''),
        ),
    ]
