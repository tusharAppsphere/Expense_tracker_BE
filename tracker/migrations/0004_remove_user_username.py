# Generated by Django 5.1.1 on 2024-12-17 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
