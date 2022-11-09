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

from .package_global import *

def index(request):
    return models(request)

@login_required
def models(request):
    all_models=model.objects.all()
    context={'models':all_models}
    return render(request,'wganbrowser/model/models.html',context)

@login_required
def detail(request,model_id):
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


