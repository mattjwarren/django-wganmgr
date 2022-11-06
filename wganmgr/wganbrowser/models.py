from django.db import models
from os import path

# Create your models here.
class library(models.Model):
    name = models.CharField(max_length=64,blank=False,unique=True)
    path = models.CharField(max_length=512,blank=False)

    def __str__(self):
        return self.name+'@'+self.path

    def path_exists(self):
        return path.isdir(self.path)

    @classmethod
    def by_strname(cls,strname):
        name=strname.split('@')[0]
        return cls.objects.get(name=name)

class dataset(models.Model):
    path = models.CharField(max_length=512,blank=False)
    name = models.CharField(max_length=255,blank=False,unique=True)
    data_first_slice = models.BooleanField(default=False)
    data_normalize = models.BooleanField(default=False)
    data_fast_wav = models.BooleanField(default=True)
    data_pad_end = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def path_exists(self):
        return path.isdir(self.path)

    @classmethod
    def by_strname(cls,strname):
        return cls.objects.get(name=strname)

class model(models.Model):
    name = models.CharField(max_length=255,blank=False,unique=True)
    library = models.ForeignKey(library,on_delete=models.CASCADE)
    dataset = models.ForeignKey(dataset,blank=False,on_delete=models.CASCADE)
    data_prefetch_gpu_num = models.IntegerField(default=0) #may need to be 1
    mode = models.CharField(max_length=32,blank=False,default='train',choices=[('train','train'),
                                                               ('preview','preview'),
                                                               ('incept','incept'),
                                                               ('infer','infer')]
                            ) 
    preview_n = models.IntegerField(default=3)

    def __str__(self):
        return str(self.library)+' : '+self.name

    @classmethod
    def by_strname(cls,strname):
        name=strname.split(':')[-1]
        return cls.objects.get(name=name)


class modelRun(models.Model):
    model = models.ForeignKey(model,blank=False,on_delete=models.CASCADE)
    path = models.CharField(max_length=512,blank=False,unique=True)
    name = models.CharField(max_length=255,blank=False,unique=True)
    train_batch_size = models.IntegerField(default=32)
    train_save_secs = models.IntegerField(default=3600)
    train_summary_secs = models.IntegerField(default=180)
    wavegan_batchnorm = models.BooleanField(default=False)
    data_num_channels = models.IntegerField(default=1)
    data_overlap_ratio = models.FloatField(default=0.0)
    data_sample_rate = models.IntegerField(default=44100)
    data_slice_len = models.IntegerField(default=65536)
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
        return str(self.model)+' : '+self.name

    def path_exists(self):
        return path.isdir(self.path)

    @classmethod
    def by_strname(cls,strname):
        name=strname.split(':')[-1]
        return cls.objects.get(name=name)


class modelSnapshot(models.Model):
    modelRun = models.ForeignKey(modelRun,blank=False,on_delete=models.CASCADE)
    checkpoint = models.IntegerField(default=0)
    d_loss_svg = models.TextField(default="")
    g_loss_svg = models.TextField(default="")
    global_step_svg = models.TextField(default="")
    #path, together with MODEL_SNAPSHOT_PACKAGES_ROOT config value should lead to the model .tar.gz
    path = models.CharField(max_length=512,blank=False,unique=True)

    def __str__(self):
        return str(self.modelRun)+' : '+str(self.checkpoint)

    def path_exists(self):
        return path.isdir(self.path)

    @classmethod
    def by_strname(cls,strname):
        library,model_name,modelrun_name,checkpoint=strname.split(':')
        return cls.objects.get(modelRun__name=name,checkpoint=checkpoint)

    #https://docs.djangoproject.com/en/4.1/intro/tutorial02/