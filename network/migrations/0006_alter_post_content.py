# Generated by Django 4.2.6 on 2023-12-28 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0005_remove_user_follower_follow_follower"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(verbose_name=""),
        ),
    ]