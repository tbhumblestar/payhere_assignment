# Generated by Django 4.1.4 on 2022-12-21 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
    ]
