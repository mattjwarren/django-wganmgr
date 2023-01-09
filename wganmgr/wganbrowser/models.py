from django.db import models
from django.conf import settings
import os

# Create your models here.
class library(models.Model):
    name = models.CharField(max_length=64,blank=False,unique=True)
    path = models.CharField(max_length=255,blank=False,unique=True,help_text="Filesystem path relative to settings.NODE_STORAGE_ROOT")
    node_affinity = models.CharField(max_length=128,default="ubuntu-wavegan-2222")

    def __str__(self):
        return self.name+'@'+self.path

    def full_path(self):
        return os.path.join(settings.NODE_STORAGE_ROOT,self.path,"")

    @classmethod
    def by_strname(cls,strname):
        name=strname.split('@')[0]
        return cls.objects.get(name=name)

class dataset(models.Model):
    #data_dir not path as used as parameter name to run command
    data_dir = models.CharField(max_length=512,blank=False,help_text="Path to dataset dir.")
    name = models.CharField(max_length=255,blank=False,unique=True)
    data_normalize = models.BooleanField(default=False,help_text="Normalize all the audio files before training?")
    data_num_channels = models.IntegerField(default=1,help_text="Channels in the audio data.")
    data_fast_wav = models.BooleanField(default=True,help_text="Use fast wav loading.")
    node_affinity = models.CharField(max_length=128,blank=True,default="ubuntu-wavegan-2222")

    def __str__(self):
        return self.name

    def full_path(self):
        return os.path.join(self.data_dir,"")

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
                                                               ('infer','infer')],
                            help_text="Run mode for model. Only train is available for now, so choose train!.") 
    preview_n = models.IntegerField(default=3,help_text="Number of audio sample previews to generate for tensorboard.")

    def __str__(self):
        return str(self.library)+' : '+self.name

    @classmethod
    def by_strname(cls,strname):
        name=strname.split(':')[-1]
        return cls.objects.get(name=name)


class modelRun(models.Model):
    model = models.ForeignKey(model,blank=False,on_delete=models.CASCADE)
    path = models.CharField(max_length=255,blank=False,unique=True,help_text="The filesystem path relative to the model library root that will store this run")
    name = models.CharField(max_length=255,blank=False,unique=True)
    comments = models.TextField(max_length=1024,default="...")
    train_batch_size = models.IntegerField(default=64,help_text="Training batch size. Smaller trains faster, but learning is more erratic. Powers of 2.")
    train_save_secs = models.IntegerField(default=3600,help_text="How often a model checkpoint is created. This is not how often a snapshot is created.")
    train_summary_secs = models.IntegerField(default=180,help_text="How often an event summary is written. This is not how often the tensorboard view is refreshed")
    wavegan_batchnorm = models.BooleanField(default=False,help_text="Should a training batch be normalized before processing?")
    data_pad_end = models.BooleanField(default=True,help_text="When training audio is shorter than slice length and using data_first_slice, pad the training audio to data_slice_len.")
    data_first_slice = models.BooleanField(default=True,help_text="Use only the first slice of each training audio sample.")
    data_overlap_ratio = models.FloatField(default=0.0,help_text="When slicing audio for training, the overlap ratio of slices.")
    data_sample_rate = models.IntegerField(default=44100,help_text="Sample rate of generated audio samples.")
    data_slice_len = models.IntegerField(default=65536,
                                        choices=[('65536','65536'),
                                                ('32768','32768'),
                                                ('16384','16384')],
                                                help_text="Slice length of audio used when training and length of generated audio samples. In samples.")
    wavegan_dim = models.IntegerField(default=64,help_text="Model dimensionality. Number of parameters the model uses to describe a sound.")
    wavegan_disc_nupdates = models.IntegerField(default=5,help_text="How many discriminator learning steps are made before making a generator learning step.")
    wavegan_disc_phaseshuffle = models.IntegerField(default=2,help_text="How much phaseshuffle is applied to the discriminator to prevent it using phase discrepancies to reject the generator.")
    wavegan_disc_wgangp_beta1 = models.FloatField(default=0.5,help_text="Adam optimizer beta1 for discriminator.")
    wavegan_disc_wgangp_beta2 = models.FloatField(default=0.9,help_text="Adam optimizer beta2 for discriminator.")
    wavegan_disc_wgangp_learn = models.FloatField(default=0.0001,help_text="Initial learning rate for discriminator.")
    wavegan_genr_pp = models.BooleanField(default=False,help_text="Does the generator also learn a noise filter?")
    wavegan_genr_pp_len = models.IntegerField(default=512,help_text="Width of the generator noise filter in samples.")
    wavegan_genr_upsample = models.CharField(max_length=32,blank=False,choices=[('zeros','zeros'),
                                                                                ('nn','nn')],
                                            help_text="Upsampling strategy used by the generator. Zeros is usually best."
    )
    wavegan_genr_wgangp_beta1 = models.FloatField(default=0.5,help_text="Adam optimizer beta1 for generator.")
    wavegan_genr_wgangp_beta2 = models.FloatField(default=0.9,help_text="Adam optimizer beta2 for generator.")
    wavegan_genr_wgangp_learn = models.FloatField(default=0.0001,help_text="Initial learning rate for generator.")
    wavegan_kernel_len = models.IntegerField(default=25,help_text="The size of the convolution window, in samples,  used by the model. Bigger may mean greater awareness of features expressed over greater time intervals.")
    wavegan_latent_dim = models.IntegerField(default=64,help_text="Latent space dimensionality. The number of dimensions to the 'space' used to map the domain of generatable sounds. Best kept the same as wavegan_dim")


    #TODO: when request modelRun, get to select which of the nodes vailable to run it on.
    #in mutlinode environment, means we rstart on the specific node because data is there
    #OR pull data over to new node from old node etc..
    node_affinity=models.CharField(max_length=128,blank=True,default="ubuntu-wavegan-2222")

    def __str__(self):
        return str(self.model)+' : '+self.name

    def full_path(self):
        return os.path.join(settings.NODE_STORAGE_ROOT,self.model.library.path,self.path,"")

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
    #path, together with MODEL_SNAPSHOT_PACKAGES_WEBROOT config value should lead to the model .tar.gz
    path = models.CharField(max_length=255,blank=True,unique=True)
    creation_time = models.DateTimeField(auto_now_add=True,blank=True)
    size_gb = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.modelRun)+' : '+str(self.checkpoint)

    def path_exists(self):
        return os.path.isdir(self.path)

    def web_path(self):
        return os.path.join(settings.MODEL_SNAPSHOT_PACKAGES_WEBROOT,self.path)
    
    def fs_path(self):
        return os.path.join(settings.MODEL_SNAPSHOT_PACKAGES_FS_ROOT,self.path)

    @classmethod
    def by_strname(cls,strname):
        library,model_name,modelrun_name,checkpoint=strname.split(':')
        return cls.objects.get(modelRun__name=modelrun_name,checkpoint=checkpoint)

    #https://docs.djangoproject.com/en/4.1/intro/tutorial02/

class x_message(models.Model):
    text=models.TextField(max_length=2048,default="")
    token=models.CharField(max_length=64,blank=False,unique=True)