# Generated by Django 4.2.3 on 2023-07-25 03:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0019_post_like_users"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="like_users",
        ),
        migrations.DeleteModel(
            name="Like",
        ),
    ]
