# Generated by Django 4.1.4 on 2022-12-21 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_user_created_at_user_updated_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="user",
            name="updated_at",
        ),
    ]
