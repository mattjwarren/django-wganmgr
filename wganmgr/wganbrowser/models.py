from django.db import models
from os import path

# Create your models here.
class library(models.Model):
    name = models.CharField(max_length=64,blank=False)
    datasets_root = models.CharField(max_length=512,blank=False)
    runs_root = models.CharField(max_length=512,blank=False)
    snapshots_root = models.CharField(max_length=512,blank=False)

    def __str__(self):
        return self.name


class dataset(models.Model):
    path = models.CharField(max_length=512,blank=False)
    name = models.CharField(max_length=512,blank=False)
    library = models.ForeignKey(library,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def path_exists(self):
        return path.isdir(self.path)

class model(models.Model):
    name = models.CharField(max_length=512,blank=False)
    library = models.ForeignKey(library,on_delete=models.CASCADE)
    dataset = models.ForeignKey(dataset,blank=False,on_delete=models.CASCADE)
    data_fast_wav = models.BooleanField(default=True)
    data_first_slice = models.BooleanField(default=False)
    data_normalize = models.BooleanField(default=False)
    data_num_channels = models.IntegerField(default=1)
    data_overlap_ratio = models.FloatField(default=0.0)
    data_pad_end = models.BooleanField(default=False)
    data_prefetch_gpu_num = models.IntegerField(default=0) #may need to be 1
    data_sample_rate = models.IntegerField(default=44100)
    data_slice_len = models.IntegerField(default=65536)
    mode = models.CharField(max_length=32,blank=False,choices=[('train','train'),
                                                               ('preview','preview'),
                                                               ('incept','incept'),
                                                               ('infer','infer')]
                            ) 
    preview_n = models.IntegerField(default=3)
    train_batch_size = models.IntegerField(default=32)
    train_save_secs = models.IntegerField(default=3600)
    train_summary_secs = models.IntegerField(default=180)
    wavegan_batchnorm = models.BooleanField(default=False)
    wavegan_dim = models.IntegerField(default=64)
    wavegan_disc_nupdates = models.IntegerField(default=5)
    wavegan_disc_phaseshuffle = models.IntegerField(default=2)
    wavegan_disc_wgangp_beta1 = models.FloatField(default=0.5)
    wavegan_disc_wgangp_beta2 = models.FloatField(default=0.9)
    wavegan_disc_wgangp_learn = models.FloatField(default=0.0001)
    wavegan_genr_pp = models.BooleanField(default=False)
    wavegan_genr_pp_len = models.IntegerField(default=512)
    wavegan_genr_upsample = models.CharField(max_length=32,blank=False,choices=[('zeros','zeros'),
                                                                                ('nn','nn')]
                                            )
    wavegan_genr_wgangp_beta1 = models.FloatField(default=0.5)
    wavegan_genr_wgangp_beta2 = models.FloatField(default=0.9)
    wavegan_genr_wgangp_learn = models.FloatField(default=0.0001)
    wavegan_kernel_len = models.IntegerField(default=25)
    wavegan_latent_dim = models.IntegerField(default=64)

    def __str__(self):
        return self.name
    
class modelRun(models.Model):
    model = models.ForeignKey(model,blank=False,on_delete=models.CASCADE)
    path = models.CharField(max_length=512,blank=False)
    name = models.CharField(max_length=512,blank=False)
    library = models.ForeignKey(library,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def path_exists(self):
        return path.isdir(self.path)

class modelSnapshot(models.Model):
    modelRun = models.ForeignKey(modelRun,blank=False,on_delete=models.CASCADE)
    checkpoint = models.IntegerField(default=0)
    path = models.CharField(max_length=512,blank=False)
    library = models.ForeignKey(library,on_delete=models.CASCADE)

    def __str__(self):
        return self.modelRun.name+'-ckpt-'+str(self.checkpoint)

    def path_exists(self):
        return path.isdir(self.path)


    #https://docs.djangoproject.com/en/4.1/intro/tutorial02/