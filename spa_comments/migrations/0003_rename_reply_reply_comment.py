# Generated by Django 4.2.8 on 2023-12-29 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa_comments', '0002_comment_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='reply',
            new_name='comment',
        ),
    ]
