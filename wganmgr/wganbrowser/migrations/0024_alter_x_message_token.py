# Generated by Django 4.1.3 on 2022-11-11 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0023_modelrun_training_node_affinity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='x_message',
            name='token',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
