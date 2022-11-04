# Generated by Django 4.1.3 on 2022-11-04 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='data_prefetch_gpu_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='model',
            name='train_save_secs',
            field=models.IntegerField(default=3600),
        ),
        migrations.AlterField(
            model_name='model',
            name='train_summary_secs',
            field=models.IntegerField(default=180),
        ),
    ]
