# Generated by Django 4.1 on 2024-01-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_organisationrequests_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='is_published',
        ),
        migrations.AddField(
            model_name='news',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('published', 'published'), ('unpublished', 'unpublished')], default='draft', max_length=250),
        ),
    ]
