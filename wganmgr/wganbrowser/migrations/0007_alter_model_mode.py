# Generated by Django 4.1.3 on 2022-11-06 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0006_alter_dataset_name_alter_model_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='mode',
            field=models.CharField(choices=[('train', 'train'), ('preview', 'preview'), ('incept', 'incept'), ('infer', 'infer')], default='train', max_length=32),
        ),
    ]