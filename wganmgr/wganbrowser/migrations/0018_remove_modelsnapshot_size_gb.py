# Generated by Django 4.1.3 on 2022-11-10 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0017_modelsnapshot_creation_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelsnapshot',
            name='size_gb',
        ),
    ]
