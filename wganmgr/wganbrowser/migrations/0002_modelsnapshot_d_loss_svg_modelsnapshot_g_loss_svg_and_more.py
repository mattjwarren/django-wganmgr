# Generated by Django 4.1.3 on 2022-11-06 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelsnapshot',
            name='d_loss_svg',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='modelsnapshot',
            name='g_loss_svg',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='modelsnapshot',
            name='global_step_svg',
            field=models.TextField(default=''),
        ),
    ]
