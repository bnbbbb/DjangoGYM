# Generated by Django 4.2.6 on 2023-11-06 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_profile_face_url_profile_insta_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
