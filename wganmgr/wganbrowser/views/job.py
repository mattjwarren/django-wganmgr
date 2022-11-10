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

from .package_global import *



@login_required
def jobs(request):
    basic_jobs=jenkins.running_builds()
    jobs=list()
    message=None
    for build,parms in basic_jobs:
        modelrun_id=int([ p.value for p in parms if p.name=='MODELRUN_ID' ][0])
        if modelrun_id>0:
            modelrun=modelRun.objects.get(pk=modelrun_id)
            jobs.append(modelrun)
        else:
            message=JOBS_UNMANAGED_JOB_IS_RUNNING
    context={'jobs':jobs,'message':message}
    return render(request,'wganbrowser/job/jobs.html',context)
