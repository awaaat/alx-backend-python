# Generated by Django 5.2.1 on 2025-06-01 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_alter_user_phone_number'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
    ]
