# Generated by Django 4.2.3 on 2023-07-18 05:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_user_address_user_city_user_town"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.CharField(
                choices=[("서울특별시", "서울특별시"), ("경기도", "경기도"), ("부산광역시", "부산광역시")],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="city",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="user",
            name="town",
            field=models.CharField(max_length=100),
        ),
    ]