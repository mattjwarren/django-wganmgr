# Generated by Django 4.1.3 on 2022-11-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0005_alter_dataset_name_alter_library_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='model',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]