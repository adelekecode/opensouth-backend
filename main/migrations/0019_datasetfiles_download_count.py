# Generated by Django 4.1 on 2024-01-05 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_datasets_geojson_alter_datasets_spatial_coverage'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetfiles',
            name='download_count',
            field=models.IntegerField(default=0),
        ),
    ]
