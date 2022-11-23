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

@login_required
def datasets(request):
    datasets=dataset.objects.all()
    context={'datasets':datasets}
    return render(request,'wganbrowser/dataset/datasets.html',context)

@login_required
def create(request):
    if request.method=='POST':
        form=datasetForm(request.POST,request.FILES)
        context={'form':form}
        if form.is_valid():
            data=form.cleaned_data
            #further validation
            if not data['node_affinity'] in settings.JENKINS_TRAINING_NODES:
                context.update({'message': DATASET_STORAGE_NODE_UNKNOWN % data['node_affinity']})
                return render(request,'wganbrowser/dataset/create.html',context)

            if bad_chars_in_path(data['data_dir']):
                context.update({'message': DATASET_BAD_CHARS_IN_PATH})
                return render(request,'wganbrowser/dataset/create.html',context)

            if not data['data_dir'].startswith(settings.NODE_DATASET_ROOT):
                if not data['data_dir'].startswith('/'):
                    data['data_dir']=os.path.join(settings.NODE_DATASET_ROOT,data['path'])
                else:
                    context.update({'message':DATASET_ABSOLUTE_PATH})
                    return render(request,'wganbrowser/dataset/create.html',context)

            if does_path_exist_on_node(data['node_affinity'],data['data_dir']):
                context.update({'message': DATASET_PATH_ALREADY_USED % data['data_dir']})
                return render(request,'wganbrowser/dataset/create.html',context)
            #create record

            new_dataset=dataset(**data)
            if handle_dataset_upload(dataset,request.FILES['dataset_file']):
                new_dataset.save()
            else:
                pass
                #problem unpakcing and saving file
    else:
        form=datasetForm()
    context={'form':form}
    return render(request,'wganbrowser/dataset/create.html',context)

@login_required
def handle_dataset_upload(dataset_record,dataset_file):
    with open('/tmp/temp_file.tar.gz','wb+') as packed_file:
        for chunk in dataset_file.chunks():
            packed_file.write(chunk)
#TODO from here

@login_required
def detail(request,dataset_id):
    return HttpResponse("Looking at details for dataset</br> %s" % str(get_object_or_404(dataset,pk=dataset_id)))
