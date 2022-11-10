from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Create your views here.
from django.http import HttpResponse
from django.template import loader

from wganbrowser.models import *
from wganbrowser.forms import *
from wganbrowser.strings import *

from time import sleep
from uuid import uuid4

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
    # '-rw-rw-r-- 1 matt matt    1361921 Nov  9 00:47 model.ckpt-6328.meta'
    print("NODE NAME IS "+node_name)
    modelrun=modelRun.objects.get(pk=modelrun_id)
    modelrun_path="%s/%s/" % (modelrun.model.library.path,modelrun.path)
    passthrough_token=str(uuid4())
    queue_item=jenkins.client.build_job(
        settings.JENKINS_PASSTHROUGH_JOB,
        TARGET_NODE=node_name,
        SQL_INSERT="insert into wganbrowser_x_messages ('text','token') values ('{%%STRING_VALUE%%}','%s')" % passthrough_token,
        SHELL_STRING="ls -ltr %s | grep ckpt | tail -1" % modelrun_path,
        JENKINS_DB_HOST_ADDRESS=settings.JENKINS_DB_HOST_ADDRESS,
        JENKINS_DB_HOST_SSH_CREDENTIALS_ID=settings.JENKINS_DB_HOST_SSH_CREDENTIALS_ID,
        JENKINS_DB_HOST_SQL_CREDENTIALS_ID=settings.JENKINS_DB_HOST_SQL_CREDENTIALS_ID,
        JENKINS_DB_HOST_SQL_DB_NAME=settings.JENKINS_DB_HOST_SQL_DB_NAME,
        JENKINS_DB_HOST_SSH_USERNAME=settings.JENKINS_DB_HOST_SSH_USERNAME
    )
    while True:
        try:
            data=x_message.objects.get(token=passthrough_token)
        except:
            data=False
        if data:
            break
        sleep(1)

    context={'job':data.text}
    return render(request,'wganbrowser/job/detail.html')


