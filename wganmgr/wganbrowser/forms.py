from django.forms import ModelForm
from .models import model as modelClass
from .models import modelRun

class modelForm(ModelForm):
    class Meta:
        model = modelClass
        fields = ['name','library','dataset']

class modelRunForm(ModelForm):
    class Meta:
        model = modelRun
        fields = ['model','path','name','train_batch_size',
                  'train_save_secs','train_summary_secs',
                  'wavegan_batchnorm','data_num_channels',
                  'data_overlap_ratio','data_sample_rate',
                  'data_slice_len','wavegan_dim','wavegan_latent_dim',
                  'wavegan_disc_nupdates','wavegan_disc_phaseshuffle',
                  'wavegan_disc_wgangp_beta1','wavegan_disc_wgangp_beta2','wavegan_disc_wgangp_learn',
                  'wavegan_genr_pp','wavegan_genr_pp_len','wavegan_genr_upsample',
                  'wavegan_genr_wgangp_beta1','wavegan_genr_wgangp_beta2','wavegan_genr_wgangp_learn',
                  'wavegan_kernel_len'
        ]
