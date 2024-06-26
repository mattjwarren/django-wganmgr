# Generated by Django 4.1.3 on 2022-11-07 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wganbrowser', '0010_alter_modelsnapshot_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelrun',
            name='comments',
            field=models.TextField(default='...', max_length=1024),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='data_fast_wav',
            field=models.BooleanField(default=True, help_text='Use fast wav loading.'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='data_normalize',
            field=models.BooleanField(default=False, help_text='Normalize all the audio files before training?'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='data_num_channels',
            field=models.IntegerField(default=1, help_text='Channels in the audio data.'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='path',
            field=models.CharField(help_text='Full filesystem path to dataset dir.', max_length=512),
        ),
        migrations.AlterField(
            model_name='library',
            name='path',
            field=models.CharField(help_text='Full filesystem path to library dir.', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='model',
            name='mode',
            field=models.CharField(choices=[('train', 'train'), ('preview', 'preview'), ('incept', 'incept'), ('infer', 'infer')], default='train', help_text='Run mode for model. Only train is available for now, so choose train!.', max_length=32),
        ),
        migrations.AlterField(
            model_name='model',
            name='preview_n',
            field=models.IntegerField(default=3, help_text='Number of audio sample previews to generate for tensorboard.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='data_first_slice',
            field=models.BooleanField(default=False, help_text='Use only the first slice of each training audio sample.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='data_overlap_ratio',
            field=models.FloatField(default=0.0, help_text='When slicing audio for training, the overlap ratio of slices.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='data_pad_end',
            field=models.BooleanField(default=False, help_text='When training audio is shorter than slice length and using data_first_slice, pad the training audio to data_slice_len.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='data_sample_rate',
            field=models.IntegerField(default=44100, help_text='Sample rate of generated audio samples.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='data_slice_len',
            field=models.IntegerField(default=65536, help_text='Slice length of audio used when training and length of generated audio samples. In samples.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='path',
            field=models.CharField(help_text='The filesystem path relative to the model library root that will store this run', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='train_batch_size',
            field=models.IntegerField(default=32, help_text='Training batch size. Smaller trains faster, but learning is more erratic. Powers of 2.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='train_save_secs',
            field=models.IntegerField(default=3600, help_text='How often a model checkpoint is created. This is not how often a snapshot is created.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='train_summary_secs',
            field=models.IntegerField(default=180, help_text='How often an event summary is written. This is not how often the tensorboard view is refreshed'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_batchnorm',
            field=models.BooleanField(default=False, help_text='Should a training batch be normalized before processing?'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_dim',
            field=models.IntegerField(default=64, help_text='Model dimensionality. Number of parameters the model uses to describe a sound.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_disc_nupdates',
            field=models.IntegerField(default=5, help_text='How many discriminator learning steps are made before making a generator learning step.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_disc_phaseshuffle',
            field=models.IntegerField(default=2, help_text='How much phaseshuffle is applied to the discriminator to prevent it using phase discrepancies to reject the generator.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_disc_wgangp_beta1',
            field=models.FloatField(default=0.5, help_text='Adam optimizer beta1 for discriminator.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_disc_wgangp_beta2',
            field=models.FloatField(default=0.9, help_text='Adam optimizer beta2 for discriminator.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_disc_wgangp_learn',
            field=models.FloatField(default=0.0001, help_text='Initial learning rate for discriminator.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_genr_pp',
            field=models.BooleanField(default=False, help_text='Does the generator also learn a noise filter?'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_genr_pp_len',
            field=models.IntegerField(default=512, help_text='Width of the generator noise filter in samples.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_genr_upsample',
            field=models.CharField(choices=[('zeros', 'zeros'), ('nn', 'nn')], help_text='Upsampling strategy used by the generator. Zeros is usually best.', max_length=32),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_genr_wgangp_beta1',
            field=models.FloatField(default=0.5, help_text='Adam optimizer beta1 for discriminator.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_genr_wgangp_beta2',
            field=models.FloatField(default=0.9, help_text='Adam optimizer beta2 for discriminator.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_genr_wgangp_learn',
            field=models.FloatField(default=0.0001, help_text='Initial learning rate for discriminator.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_kernel_len',
            field=models.IntegerField(default=25, help_text='The size of the convolution window, in samples,  used by the model. Bigger may mean greater awareness of features expressed over greater time intervals.'),
        ),
        migrations.AlterField(
            model_name='modelrun',
            name='wavegan_latent_dim',
            field=models.IntegerField(default=64, help_text="Latent space dimensionality. The number of dimensions to the 'space' used to map the domain of generatable sounds. Best kept the same as wavegan_dim"),
        ),
    ]
