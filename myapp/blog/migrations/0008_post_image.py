# Generated by Django 4.2.3 on 2023-07-19 04:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0007_alter_tag_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(default=1, upload_to="blog/media/"),
            preserve_default=False,
        ),
    ]