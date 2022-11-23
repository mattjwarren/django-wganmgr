from django.conf import settings
from wganbrowser.jenkins_api import *
from wganbrowser.models import *
from wganbrowser.shell_strings import *

from uuid import uuid4
from time import sleep
import re

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


def waitfor_queryset(wait_period,query_set,max_waits=9999999):
    wait_count=0
    while True:
        if wait_count<max_waits:
            if len(query_set)>0:#forces evaluation
                return query_set
            else:
                sleep(wait_period)
                query_set=query_set.all()#forces result cache refresh
                wait_count+=1
        else:
            break
    return None

def exec_shell(node_name,shell_string):
    passthrough_token=str(uuid4())
    job_parameters={
        'TARGET_NODE':node_name,
        'SQL_INSERT':"insert into wganbrowser_x_message (text,token) values ('{%%STRING_VALUE%%}','%s');" % passthrough_token,
        'SHELL_STRING':shell_string,
        'JENKINS_DB_HOST_ADDRESS':settings.JENKINS_DB_HOST_ADDRESS,
        'JENKINS_DB_HOST_SSH_CREDENTIALS_ID':settings.JENKINS_DB_HOST_SSH_CREDENTIALS_ID,
        'JENKINS_DB_HOST_SQL_CREDENTIALS_ID':settings.JENKINS_DB_HOST_SQL_CREDENTIALS_ID,
        'JENKINS_DB_HOST_SQL_DB_NAME':settings.JENKINS_DB_HOST_SQL_DB_NAME,
        'JENKINS_DB_HOST_SSH_USERNAME':settings.JENKINS_DB_HOST_SSH_USERNAME
    }
    queue_item=jenkins.build(
        settings.JENKINS_PASSTHROUGH_JOB,
        job_parameters
    )
    query_set=x_message.objects.all().filter(token=passthrough_token)
    
    query_set=waitfor_queryset(1,query_set,30)
    if query_set:
        x_msg=query_set.get()
        stdout=x_msg.text
        x_msg.delete()
    else:
        stdout=""
    return stdout


#TODO: see regroup template tag (or dont, see ordering problem)
#https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#regroup
def group_records_by_field(records,field_names):
    grouped_dict=dict()
    for record in records:
        field_val=record
        for field_name in field_names:
            field_val=getattr(field_val,field_name)
        if not field_val in grouped_dict:
            grouped_dict[field_val]=[record]
        else:
            grouped_dict[field_val].append(record)
    return grouped_dict

def bad_chars_in_path(path):
    return re.match(".*[^A-Za-z0-9_/-].*",path)

#shell execs

def does_path_exist_on_node(node,path):
    return exec_shell(node,SHELL_DOES_PATH_EXIST % path)=="True"

def create_path_on_node(node,path):
    return exec_shell(node, SHELL_MKDIR_P % path)=="True"

def move_path(node,from_path,to_path):
    return exec_shell(node, SHELL_MV % (from_path,to_path))=="True"



