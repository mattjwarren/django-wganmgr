from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import *
from .forms import *
from .jenkins_client import *

def index(request):
    return models(request)


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


@login_required
def models(request):
    all_models=model.objects.all()
    context={'models':all_models}
    return render(request,'wganbrowser/model/models.html',context)

@login_required
def model_detail(request,model_id):
    selected_model = model.objects.get(pk=model_id)
    runs = modelRun.objects.filter(model=selected_model)

    runs_with_snapshot=dict()
    for run in runs:
        latest_snapshot=None
        latest_snapshots=modelSnapshot.objects.filter(modelRun=run.id).order_by('-checkpoint')
        if(latest_snapshots.count()>0):
            latest_snapshot=latest_snapshots[0]
        runs_with_snapshot[run]=latest_snapshot

    context={
        'model_id':model_id,
        'model':selected_model,
        'runs_with_snapshot':runs_with_snapshot,
    }

    return render(request,'wganbrowser/model/model_detail.html',context)

@login_required
def model_create(request):
    form = modelForm()
    context = {'form':form} 
    return render(request,'wganbrowser/model/model_create.html',context)

@login_required
def model_save(request):
    if request.method=='POST':
        form=modelForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            new_model=model(name=data['name'],
                            library=data['library'],
                            dataset=data['dataset'])
            new_model.save()
            return models(request)
    else:
        return model_create(request)

@login_required
def model_delete(request,model_id):
    selected_model = model.objects.get(pk=model_id)
    if selected_model:
        selected_model.delete()
    return models(request)

@login_required
def dataset_detail(request,dataset_id):
    return HttpResponse("Looking at details for dataset</br> %s" % str(get_object_or_404(dataset,pk=dataset_id)))

@login_required
def modelruns(request):
    all_modelruns=modelRun.objects.all()
    context={'modelruns':all_modelruns}
    return render(request,'wganbrowser/modelrun/modelruns.html',context)

@login_required
def modelrun_detail(request,modelrun_id):
    modelrun = modelRun.objects.get(pk=modelrun_id)
    modelsnapshots = modelSnapshot.objects.filter(modelRun=modelrun)

    context={
        'modelrun_id':modelrun_id,
        'modelrun':modelrun,
        'modelsnapshots':modelsnapshots,
    }

    return render(request,'wganbrowser/modelrun/modelrun_detail.html',context)

@login_required
def modelrun_create(request):
    form = modelRunForm()
    context = {'form':form} 
    return render(request,'wganbrowser/modelrun/modelrun_create.html',context)

@login_required
def modelrun_save(request):
    if request.method=='POST':
        form=modelRunForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            new_modelrun=modelRun(model=data['model'],
                               path=data['path'],
                               name=data['name'],
                               comments=data['comments'],
                               train_batch_size=data['train_batch_size'],
                               train_save_secs=data['train_save_secs'],
                               train_summary_secs=data['train_summary_secs'],
                               wavegan_batchnorm=data['wavegan_batchnorm'],
                               data_pad_end=data['data_pad_end'],
                               data_first_slice=data['data_first_slice'],
                               data_overlap_ratio=data['data_overlap_ratio'],
                               data_sample_rate=data['data_sample_rate'],
                               data_slice_len=data['data_slice_len'],
                               wavegan_dim=data['wavegan_dim'],
                               wavegan_latent_dim=data['wavegan_latent_dim'],
                               wavegan_disc_nupdates=data['wavegan_disc_nupdates'],
                               wavegan_disc_phaseshuffle=data['wavegan_disc_phaseshuffle'],
                               wavegan_disc_wgangp_beta1=data['wavegan_disc_wgangp_beta1'],
                               wavegan_disc_wgangp_beta2=data['wavegan_disc_wgangp_beta2'],
                               wavegan_disc_wgangp_learn=data['wavegan_disc_wgangp_learn'],
                               wavegan_genr_pp=data['wavegan_genr_pp'],
                               wavegan_genr_pp_len=data['wavegan_genr_pp_len'],
                               wavegan_genr_upsample=data['wavegan_genr_upsample'],
                               wavegan_genr_wgangp_beta1=data['wavegan_genr_wgangp_beta1'],
                               wavegan_genr_wgangp_beta2=data['wavegan_genr_wgangp_beta2'],
                               wavegan_genr_wgangp_learn=data['wavegan_genr_wgangp_learn'],
                               wavegan_kernel_len=data['wavegan_kernel_len']
            )
            new_modelrun.save()
            return modelruns(request)
    else:
        return modelrun_create(request)

@login_required
def modelrun_delete(request,modelrun_id):
    modelrun = modelRun.objects.get(pk=modelrun_id)
    if modelrun:
        modelrun.delete()
    return modelruns(request)

@login_required
def modelrun_request(request,modelrun_id):
    modelrun = modelRun.objects.get(pk=modelrun_id)
    modelrun_request_form = modelRunRequestForm(initial={'modelrun_id':modelrun.id})
    context={'form':modelrun_request_form,'modelrun':modelrun}
    return render(request,'wganbrowser/modelrun/modelrun_request.html',context)

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

@login_required
def modelrun_post(request):
    if request.method=='POST':
        form=modelRunRequestForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            modelrun = modelRun.objects.get(pk=data['modelrun_id'])
            jc=client(settings.JENKINS_URL,auth=(settings.JENKINS_USER,settings.JENKINS_PWD))
            #
            # TODO: all sorts of checking nothing is running
            run_command_args=build_run_command_args_from_modelrun(modelrun)
            build_job=jc.build_job(settings.JENKINS_TRAIN_JOB,
                                    WAVEGAN_REPO_ROOT=settings.JENKINS_WAVEGAN_REPO_ROOT,
                                    UPLOAD_INTERVAL=data['upload_interval'],
                                    MODEL_UPLOAD_INTERVAL_TYPE=data['model_upload_interval_type'],
                                    TENSORBOARD_REFRESH_INTERVAL=data['tensorboard_refresh_interval'],
                                    BOARD_REFRESH_INTERVAL_TYPE=data['board_refresh_interval_type'],
                                    RUNS_ROOT=modelrun.model.library.path,
                                    MODEL=modelrun.path,
                                    RUN_COMMAND_ARGS=run_command_args,
                                    PYTHON_VENV_ACTIVATE=settings.JENKINS_PYENV_ACTIVATE,
                                    WGANMGR_REQUEST=True,
                                    MODELRUN_ID=modelrun.id)
            #TODO: render jenkins job view
            return modelruns(request)
        else:
            #TODO: render bad form message and go to modelrun_request
            return modelruns(request)
    else:
        return modelruns(request)


@login_required
def modelsnapshot_detail(request,modelsnapshot_id):
    return HttpResponse("Looking at details for modelsnapshot</br> %s" % str(get_object_or_404(modelSnapshot,pk=modelsnapshot_id)))

@login_required
def library_detail(request,library_id):
    return HttpResponse("Looking at details for library</br> %s" % str(get_object_or_404(library,pk=library_id)))

