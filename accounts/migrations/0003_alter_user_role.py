# Generated by Django 4.1 on 2024-01-20 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('moderator', 'Moderator')], max_length=255, verbose_name='role'),
        ),
    ]
