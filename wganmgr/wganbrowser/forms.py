from django.forms import ModelForm
from .models import model as modelClass
from .models import modelRun
from django import forms

class modelForm(ModelForm):
    class Meta:
        model = modelClass
        fields = ['name','library','dataset']

class modelRunForm(ModelForm):
    class Meta:
        model = modelRun
        fields = ['name','model','path','comments','train_batch_size',
                  'train_save_secs','train_summary_secs',
                  'wavegan_batchnorm','data_sample_rate',
                  'data_slice_len','data_first_slice','data_pad_end',
                  'data_overlap_ratio','wavegan_dim','wavegan_latent_dim',
                  'wavegan_disc_nupdates','wavegan_disc_phaseshuffle',
                  'wavegan_genr_upsample','wavegan_genr_pp','wavegan_genr_pp_len','wavegan_kernel_len',
                  'wavegan_disc_wgangp_beta1','wavegan_disc_wgangp_beta2','wavegan_disc_wgangp_learn',
                  'wavegan_genr_wgangp_beta1','wavegan_genr_wgangp_beta2','wavegan_genr_wgangp_learn'
                  
        ]

class modelRunRequestForm(forms.Form):
    upload_interval = forms.IntegerField(initial=5000,
        help_text="""When model upload interval type is CHECKPOINT
                     then once the most recently generated checkpoint is
                     at least 'Upload Interval' checkpoints from the last
                     published snapshot, a new snapshot will be published.
                     When the upload interval type is SECONDS, a new
                     snapshot will be generated every 'Upload Interval' seconds.
                     Checkpoints are generated every ModelRun.train_save_secs
                     seconds.""")
    model_upload_interval_type = forms.ChoiceField(initial='CHECKPOINT',
        choices=[("CHECKPOINT","CHECKPOINT"),
                 ("SECONDS","SECONDS")])
    tensorboard_refresh_interval = forms.IntegerField(initial=180,
        help_text="""Works like upload_interval, controls when the tensorboard
                     info for the run is refreshed. New tensorboard events
                     are generated every ModelRun.train_summary_secs
                     seconds.""")
    board_refresh_interval_type = forms.ChoiceField(initial='SECONDS',
        choices=[("CHECKPOINT","CHECKPOINT"),
                 ("SECONDS","SECONDS")])
    modelrun_id = forms.IntegerField(widget=forms.HiddenInput())
    #runs_root - model library root
    #model - model_run path
    #run_command_args - generated from model,dataset,modelrun fields
    #dont forget set inital on modelrun_id
    #https://stackoverflow.com/questions/46941694/how-do-i-populate-a-hidden-required-field-in-django-forms

