# Generated by Django 4.2.3 on 2023-07-18 04:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_user_business"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BusinessUser",
        ),
    ]