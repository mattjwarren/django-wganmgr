from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Create your views here.
from django.http import HttpResponse
from django.template import loader

from wganbrowser.models import *
from wganbrowser.forms import *
from wganbrowser.jenkins_api import *
from wganbrowser.strings import *

from time import sleep

#from jobs import jobs
from wganbrowser.views import job

from .package_global import *

@login_required
def modelruns(request):
    modelruns=modelRun.objects.all()
    modelruns=group_records_by_field(modelruns,['model','name'])
    context={'modelruns':modelruns}
    return render(request,'wganbrowser/modelrun/modelruns.html',context)

@login_required
def detail(request,modelrun_id):
    modelrun = modelRun.objects.get(pk=modelrun_id)
    modelsnapshots = modelSnapshot.objects.filter(modelRun=modelrun)

    context={
        'modelrun_id':modelrun_id,
        'modelrun':modelrun,
        'modelsnapshots':modelsnapshots,
    }

    return render(request,'wganbrowser/modelrun/detail.html',context)

@login_required
def create(request):
    form = modelRunForm()
    context = {'form':form} 
    return render(request,'wganbrowser/modelrun/create.html',context)

@login_required
def save(request):
    if request.method=='POST':
        form=modelRunForm(request.POST)
        context={'form':form}
        if form.is_valid():
            data=form.cleaned_data

            #TODO path validation
            if not data['node_affinity'] in settings.JENKINS_TRAINING_NODES:
                context.update({'message': LIBRARY_STORAGE_NODE_UNKNOWN % data['node_affinity']})
                return render(request,'wganbrowser/modelrun/create.html',context)

            if bad_chars_in_path(data['path']):
                context.update({'message': MODELRUN_BAD_CHARS_IN_PATH})
                return render(request,'wganbrowser/modelrun/create.html',context)                

            if data['path'].startswith('/'):
                context.update({'message': MODELRUN_ABSOLUTE_PATH})
                return render(request,'wganbrowser/modelrun/create.html',context)

            full_path=os.path.join(settings.NODE_STORAGE_ROOT,data['path'],"")

            if does_path_exist_on_node(data['node_affinity'],full_path):
                context.update({'message': MODELRUN_PATH_ALREADY_USED % data['path']})
                return render(request,'wganbrowser/modelrun/create.html',context)

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
                                    wavegan_kernel_len=data['wavegan_kernel_len'],
                                    node_affinity=data['node_affinity']
            )
            new_modelrun.save()
            return modelruns(request)
    else:
        return create(request)

@login_required
def delete(request,modelrun_id):
    modelrun = modelRun.objects.get(pk=modelrun_id)
    if modelrun:
        modelrun.delete()
    return modelruns(request)

@login_required
def request(request,modelrun_id):
    modelrun = modelRun.objects.get(pk=modelrun_id)
    request_form = modelRunRequestForm(initial={'modelrun_id':modelrun.id})
    context={'form':request_form,'modelrun':modelrun}
    return render(request,'wganbrowser/modelrun/request.html',context)

@login_required
def post(request):
    if request.method=='POST':
        form=modelRunRequestForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            modelrun = modelRun.objects.get(pk=data['modelrun_id'])

            if jenkins.is_running(settings.JENKINS_TRAIN_JOB):
                context={'form':form,'modelrun':modelrun,
                        'message':MODELRUN_POST_ALREADY_RUNNING}
                return render(request,'wganbrowser/modelrun/request.html',context)

            run_command_args=build_run_command_args_from_modelrun(modelrun)
            job_parameters={
                'WAVEGAN_REPO_ROOT':settings.JENKINS_WAVEGAN_REPO_ROOT,
                'UPLOAD_INTERVAL':data['upload_interval'],
                'MODEL_UPLOAD_INTERVAL_TYPE':data['model_upload_interval_type'],
                'TENSORBOARD_REFRESH_INTERVAL':data['tensorboard_refresh_interval'],
                'BOARD_REFRESH_INTERVAL_TYPE':data['board_refresh_interval_type'],
                'RUNS_ROOT':modelrun.model.library.full_path(),
                'MODEL':modelrun.path,
                'RUN_COMMAND_ARGS':run_command_args,
                'PYTHON_VENV_ACTIVATE':settings.JENKINS_PYENV_ACTIVATE,
                'WGANMGR_REQUEST':True,
                'MODELRUN_ID':modelrun.id
            }
            queue_item=jenkins.build(
                settings.JENKINS_TRAIN_JOB,
                job_parameters
            )
            sleep(3)
            jobs,message=job.get_jobs()
            messages=list()
            if message:
                messages.append(message)
            messages.append(JOBS_JOB_REQUESTED % modelrun.name)
            context={'jobs':jobs,'messages':messages}
            return render(request,'wganbrowser/job/jobs.html',context)
        else:
            #TODO: render bad form message and go to modelrun_request
            return modelruns(request)
    else:
        return modelruns(request)