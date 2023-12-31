# Generated by Django 4.2.3 on 2023-07-25 03:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0020_remove_post_like_users_delete_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="like_users",
            field=models.ManyToManyField(
                related_name="liked_posts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
