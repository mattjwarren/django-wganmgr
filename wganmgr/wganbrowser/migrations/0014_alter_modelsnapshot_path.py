# Generated by Django 4.1.3 on 2022-11-09 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0013_modelsnapshot_creation_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelsnapshot',
            name='path',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
