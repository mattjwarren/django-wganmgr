# Generated by Django 4.1.3 on 2022-11-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0008_remove_dataset_data_first_slice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='path',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='path',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
