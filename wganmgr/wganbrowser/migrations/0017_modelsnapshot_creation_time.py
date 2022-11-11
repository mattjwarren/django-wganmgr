# Generated by Django 4.1.3 on 2022-11-10 19:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0016_remove_modelsnapshot_creation_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelsnapshot',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]