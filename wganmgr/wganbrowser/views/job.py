from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Create your views here.
from django.http import HttpResponse
from django.template import loader

from wganbrowser.models import *
from wganbrowser.forms import *
from wganbrowser.strings import *
from wganbrowser.shell_strings import *

from time import sleep
from datetime import datetime
import math
import os

from .package_global import *


def get_jobs():
    basic_jobs=jenkins.running_builds()
    jobs=list()
    message=None
    for build,parms,node_name in basic_jobs:
        modelrun_id=int([ p.value for p in parms if p.name=='MODELRUN_ID' ][0])
        if modelrun_id>0:
            modelrun=modelRun.objects.get(pk=modelrun_id)
            jobs.append({'modelrun':modelrun,'node_name':node_name})
        else:
            message=JOBS_UNMANAGED_JOB_IS_RUNNING
    return (jobs,message)


@login_required
def jobs(request):
    jobs,message=get_jobs()
    context={'jobs':jobs,'message':message}
    return render(request,'wganbrowser/job/jobs.html',context)

def detail(request,modelrun_id,node_name):
    modelrun=modelRun.objects.get(pk=modelrun_id)

    if not jenkins.modelrun_is_running(modelrun_id):
        jobs,message=get_jobs()
        messages=list()
        if message:
            messages.append(message)
        messages.append(JOBS_JOB_NOT_FOUND % modelrun.name)
        context={'jobs':jobs,'messages':messages}
        return render(request,'wganbrowser/job/jobs.html',context)

    #New jobs take a few seconds to write the first checkpoint file
    ckpt_found=False
    while not ckpt_found:
        query_text=exec_shell(node_name,SHELL_GET_NEWEST_CKPT_FILE % modelrun.full_path())
        tokens=query_text.split()
        try:
            date_time_str=("%s %s" % tuple(tokens[5:7])).split('.')[0]
        except:
            sleep(1)
            continue
        ckpt_found=True

    train_ckpt_date=datetime.strptime(date_time_str,'%Y-%m-%d %H:%M:%S')
    train_ckpt_timedelta=round((modelrun.train_save_secs-((datetime.now()-train_ckpt_date).total_seconds()))/60,1)
    if train_ckpt_timedelta<0:
        train_ckpt_timedelta=round(modelrun.train_save_secs/60,1)
    latest_ckpt=tokens[8].split('-')[1].split('.')[0]

    latest_snapshots=modelSnapshot.objects.filter(modelRun=modelrun.id).order_by('-checkpoint')
    latest_snapshot=None

    if latest_snapshots:
        latest_snapshot=latest_snapshots[0]
    
    snapshot_interval_type=None
    snapshot_interval=0

    basic_jobs=jenkins.running_builds()
    for build,parms,node_name in basic_jobs:
        for parm in parms:
            if parm.name=='MODELRUN_ID' and int(parm.value)==modelrun_id:
                snapshot_interval_type=[ p.value for p in parms if p.name=='MODEL_UPLOAD_INTERVAL_TYPE' ][0]
                snapshot_interval=int([ p.value for p in parms if p.name=='UPLOAD_INTERVAL' ][0])

    if latest_snapshot and snapshot_interval_type=='CHECKPOINT':
        snapshot_delta=int(latest_ckpt)-latest_snapshot.checkpoint
    elif latest_snapshot and snapshot_interval_type=='SECONDS':
        snapshot_delta=(datetime.now()-latest_snapshot.creation_time).total_seconds()
    else:
        snapshot_delta=0

    context={'modelrun':modelrun,
             'latest_checkpoint':latest_ckpt,
             'latest_train_checkpoint_datetime':train_ckpt_date,
             'train_save_secs':modelrun.train_save_secs,
             'training_ckpt_timedelta':train_ckpt_timedelta,
             'latest_snapshot':latest_snapshot,
             'snapshot_interval_type':snapshot_interval_type,
             'snapshot_interval':snapshot_interval,
             'snapshot_delta':snapshot_delta,
             'node_name':node_name}

    return render(request,'wganbrowser/job/detail.html',context)

def halt(request,modelrun_id,node_name):
    jobs,message=get_jobs()
    modelrun=modelRun.objects.get(pk=modelrun_id)
    touch_halt=exec_shell(node_name,SHELL_TOUCH_HALT % modelrun.full_path())
    messages=list()
    if message:
        messages.append(message)
    messages.append(JOBS_JOB_WILL_HALT % modelrun.name)
    context={'jobs':jobs,'messages':messages}
    return render(request,'wganbrowser/job/jobs.html',context)

def force_model_snapshot(request,modelrun_id,node_name):
    jobs,message=get_jobs()
    modelrun=modelRun.objects.get(pk=modelrun_id)
    touch_upload_model=exec_shell(node_name,SHELL_TOUCH_UPLOAD_MODEL % modelrun.full_path())
    messages=list()
    if message:
        messages.append(message)
    messages.append(JOBS_JOB_WILL_UPLOAD_MODEL % modelrun.name)
    context={'jobs':jobs,'messages':messages}
    return render(request,'wganbrowser/job/jobs.html',context)

def console_log(request,modelrun_id,node_name):
    modelrun=modelRun.objects.get(pk=modelrun_id)
    context={'modelrun':modelrun,
            'node_name':node_name}

    build=jenkins.get_modelrun_build(modelrun_id)
    if not build:
        context.update({'message': JOBS_JOB_NOT_FOUND % modelrun.name})
        return (request,'wganbrowser/job/console_log.html',context)
    jenkins_log='\n'.join([ line.decode() for line in build.console_text() if b'[Pipeline]' not in line ])

    context.update({'jenkins_log':jenkins_log})
    return render(request,'wganbrowser/job/console_log.html',context)






