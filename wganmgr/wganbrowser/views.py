from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import *
from .forms import *

def index(request):
    return models(request)

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
def modelsnapshot_detail(request,modelsnapshot_id):
    return HttpResponse("Looking at details for modelsnapshot</br> %s" % str(get_object_or_404(modelSnapshot,pk=modelsnapshot_id)))

@login_required
def library_detail(request,library_id):
    return HttpResponse("Looking at details for library</br> %s" % str(get_object_or_404(library,pk=library_id)))

