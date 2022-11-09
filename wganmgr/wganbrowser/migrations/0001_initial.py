# Generated by Django 4.1.3 on 2022-11-05 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=512)),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('path', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('data_fast_wav', models.BooleanField(default=True)),
                ('data_first_slice', models.BooleanField(default=False)),
                ('data_normalize', models.BooleanField(default=False)),
                ('data_num_channels', models.IntegerField(default=1)),
                ('data_overlap_ratio', models.FloatField(default=0.0)),
                ('data_pad_end', models.BooleanField(default=False)),
                ('data_prefetch_gpu_num', models.IntegerField(default=0)),
                ('data_sample_rate', models.IntegerField(default=44100)),
                ('data_slice_len', models.IntegerField(default=65536)),
                ('mode', models.CharField(choices=[('train', 'train'), ('preview', 'preview'), ('incept', 'incept'), ('infer', 'infer')], max_length=32)),
                ('preview_n', models.IntegerField(default=3)),
                ('train_batch_size', models.IntegerField(default=32)),
                ('train_save_secs', models.IntegerField(default=3600)),
                ('train_summary_secs', models.IntegerField(default=180)),
                ('wavegan_batchnorm', models.BooleanField(default=False)),
                ('wavegan_dim', models.IntegerField(default=64)),
                ('wavegan_disc_nupdates', models.IntegerField(default=5)),
                ('wavegan_disc_phaseshuffle', models.IntegerField(default=2)),
                ('wavegan_disc_wgangp_beta1', models.FloatField(default=0.5)),
                ('wavegan_disc_wgangp_beta2', models.FloatField(default=0.9)),
                ('wavegan_disc_wgangp_learn', models.FloatField(default=0.0001)),
                ('wavegan_genr_pp', models.BooleanField(default=False)),
                ('wavegan_genr_pp_len', models.IntegerField(default=512)),
                ('wavegan_genr_upsample', models.CharField(choices=[('zeros', 'zeros'), ('nn', 'nn')], max_length=32)),
                ('wavegan_genr_wgangp_beta1', models.FloatField(default=0.5)),
                ('wavegan_genr_wgangp_beta2', models.FloatField(default=0.9)),
                ('wavegan_genr_wgangp_learn', models.FloatField(default=0.0001)),
                ('wavegan_kernel_len', models.IntegerField(default=25)),
                ('wavegan_latent_dim', models.IntegerField(default=64)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wganbrowser.dataset')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wganbrowser.library')),
            ],
        ),
        migrations.CreateModel(
            name='modelRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=512)),
                ('name', models.CharField(max_length=512)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wganbrowser.model')),
            ],
        ),
        migrations.CreateModel(
            name='modelSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkpoint', models.IntegerField(default=0)),
                ('path', models.CharField(max_length=512)),
                ('modelRun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wganbrowser.modelrun')),
            ],
        ),
    ]