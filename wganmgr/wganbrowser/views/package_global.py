from django.conf import settings
from wganbrowser.jenkins_api import *

jenkins=jenkins_helper(settings.JENKINS_URL,auth=(settings.JENKINS_USER,settings.JENKINS_PWD))

accepted_args="""[--data_dir DATA_DIR dd]
                [--data_sample_rate DATA_SAMPLE_RATE dsr ]
                [--data_slice_len {16384,32768,65536} dsl ]
                [--data_num_channels DATA_NUM_CHANNELS dnc ]
                [--data_overlap_ratio DATA_OVERLAP_RATIO dor ]
                [--data_first_slice BOOL dfs ]
                [--data_pad_end BOOL dpe ]
                [--data_normalize BOOL dn ]
                [--data_fast_wav BOOL dfw ]
                [--data_prefetch_gpu_num DATA_PREFETCH_GPU_NUM ~ ]
                [--wavegan_latent_dim WAVEGAN_LATENT_DIM wld ]
                [--wavegan_kernel_len WAVEGAN_KERNEL_LEN wkl ]
                [--wavegan_dim WAVEGAN_DIM wd ]
                [--wavegan_batchnorm BOOL wb ]
                [--wavegan_disc_nupdates WAVEGAN_DISC_NUPDATES dnup ]
                [--wavegan_loss {dcgan,lsgan,wgan,wgan-gp} wl ]
                [--wavegan_genr_upsample {zeros,nn} wups ]
                [--wavegan_genr_pp BOOL wgp ]
                [--wavegan_genr_pp_len WAVEGAN_GENR_PP_LEN wppl ]
                [--wavegan_disc_phaseshuffle WAVEGAN_DISC_PHASESHUFFLE wdps ]
                [--wavegan_genr_wgangp_learn WAVEGAN_GENR_WGANGP_LEARN wgwl ]
                [--wavegan_genr_wgangp_beta1 WAVEGAN_GENR_WGANGP_BETA1 wgba ]
                [--wavegan_genr_wgangp_beta2 WAVEGAN_GENR_WGANGP_BETA2 wgbb ]
                [--wavegan_disc_wgangp_learn WAVEGAN_DISC_WGANGP_LEARN wdwl ]
                [--wavegan_disc_wgangp_beta1 WAVEGAN_DISC_WGANGP_BETA1 wdba ]
                [--wavegan_disc_wgangp_beta2 WAVEGAN_DISC_WGANGP_BETA2 wdbb ]
                [--train_batch_size TRAIN_BATCH_SIZE tbs ]
                [--train_save_secs TRAIN_SAVE_SECS tss ]
                [--train_summary_secs TRAIN_SUMMARY_SECS tsums ]
                [--preview_n PREVIEW_N pn ]
                [--incept_metagraph_fp INCEPT_METAGRAPH_FP ~ ]
                [--incept_ckpt_fp INCEPT_CKPT_FP ~ ]
                [--incept_n INCEPT_N ~ ]
                [--incept_k INCEPT_K ~ ]"""

def iterate_record_for_run_command_args(record):
    run_command_args=""
    for field in record._meta.get_fields():
        if "--"+field.name in accepted_args:
            arg_part=getattr(record,field.name)
            if arg_part is True:
                arg_part=""
            elif arg_part is False:
                continue
            run_command_args+=" --%s %s" % (field.name,arg_part)
    return run_command_args

def build_run_command_args_from_modelrun(modelrun):
    run_command_args=""
    run_command_args+=iterate_record_for_run_command_args(modelrun)
    run_command_args+=iterate_record_for_run_command_args(modelrun.model)
    run_command_args+=iterate_record_for_run_command_args(modelrun.model.dataset)
    return run_command_args