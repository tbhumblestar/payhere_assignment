# Generated by Django 4.1.4 on 2022-12-21 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_user_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
    ]
