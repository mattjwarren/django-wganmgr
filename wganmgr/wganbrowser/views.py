from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import *

def index(request):
    return HttpResponse("Hello, world. You're at the wgan browser index.")

def model_detail(request,model_id):
    selected_model = model.objects.get(pk=model_id)
    runs = modelRun.objects.filter(model=model_id)

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

def dataset_detail(request,dataset_id):
    return HttpResponse("Looking at details for dataset</br> %s" % str(get_object_or_404(dataset,pk=dataset_id)))

def modelrun_detail(request,modelrun_id):
    return HttpResponse("Looking at details for modelrun</br> %s" % str(get_object_or_404(modelRun,pk=modelrun_id)))

def modelsnapshot_detail(request,modelsnapshot_id):
    return HttpResponse("Looking at details for modelsnapshot</br> %s" % str(get_object_or_404(modelSnapshot,pk=modelsnapshot_id)))

def library_detail(request,library_id):
    return HttpResponse("Looking at details for library</br> %s" % str(get_object_or_404(library,pk=library_id)))

