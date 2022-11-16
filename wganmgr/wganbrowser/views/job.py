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

from .package_global import *



@login_required
def jobs(request):
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
    context={'jobs':jobs,'message':message}
    return render(request,'wganbrowser/job/jobs.html',context)

def detail(request,modelrun_id,node_name):
    #we need,
    #modelrun instance
    #vi apassthorugh: last training checkpoint written and date/time
    #  -   ls -ltr {library_root}/{modelrun_path}/ | grep ckpt | tail -1
    # '-rw-rw-r-- 1 matt matt       3530 2022-11-11 02:56:39.869787709 +0000 model.ckpt-22280.index'
    modelrun=modelRun.objects.get(pk=modelrun_id)
    modelrun_path="%s/%s/" % (modelrun.model.library.path,modelrun.path)
    query_text=exec_shell(node_name,SHELL_GET_NEWEST_CKPT_FILE % modelrun_path)
    tokens=query_text.split()
    date_time_str=("%s %s" % tuple(tokens[5:7])).split('.')[0]

    dateobject=datetime.strptime(date_time_str,'%Y-%m-%d %H:%M:%S')
    training_ckpt_timedelta=round((modelrun.train_save_secs-((datetime.now()-dateobject).total_seconds()))/60,1)
    latest_ckpt=tokens[8].split('-')[1].split('.')[0]
    latest_snapshots=modelSnapshot.objects.filter(modelRun=modelrun.id).order_by('-checkpoint')
    latest_snapshot=None
    if(latest_snapshots.count()>0):
        latest_snapshot=latest_snapshots[0]
    
    snapshot_interval_type="SECONDS"

    basic_jobs=jenkins.running_builds()
    for build,parms,node_name in basic_jobs:
        for parm in parms:
            if parm.name=='MODELRUN_ID' and int(parm.value)==modelrun_id:
                snapshot_interval_type=[ p.value for p in parms if p.name=='MODEL_UPLOAD_INTERVAL_TYPE' ][0]
                snapshot_interval=int([ p.value for p in parms if p.name=='UPLOAD_INTERVAL' ][0])

    if snapshot_interval_type=='CHECKPOINT':
        snapshot_delta=int(latest_ckpt)-latest_snapshot.checkpoint
    else:
        snapshot_delta=9999

    context={'modelrun':modelrun,
             'latest_checkpoint':latest_ckpt,
             'latest_train_checkpoint_datetime':dateobject,
             'train_save_secs':modelrun.train_save_secs,
             'training_ckpt_timedelta':training_ckpt_timedelta,
             'latest_snapshot':latest_snapshot,
             'snapshot_interval_type':snapshot_interval_type,
             'snapshot_interval':snapshot_interval,
             'snapshot_delta':snapshot_delta}

    return render(request,'wganbrowser/job/detail.html',context)


