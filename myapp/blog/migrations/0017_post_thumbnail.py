# Generated by Django 4.2.3 on 2023-07-24 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0016_alter_post_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to="blog/media"),
        ),
    ]