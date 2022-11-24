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
from uuid import uuid4

from .package_global import *

@login_required
def datasets(request):
    datasets=dataset.objects.all()
    context={'datasets':datasets}
    return render(request,'wganbrowser/dataset/datasets.html',context)

@login_required
def create(request):
    context={}
    if request.method=='POST':
        form=datasetForm(request.POST,request.FILES)
        print("FILES: %s" % len(request.FILES))
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

            new_dataset=dataset(name=data['name'], data_dir=data['data_dir'], data_normalize=data['data_normalize'],
                                data_num_channels=data['data_num_channels'],
                                data_fast_wav=data['data_fast_wav'],
                                node_affinity=data['node_affinity'])
            if handle_dataset_upload(request,new_dataset,request.FILES['dataset_file']):
                new_dataset.save()
                return datasets(request)
            else:
                context.update({'message':DATASET_ERROR_RECEIVING_AND_UNPACKING})
                return render(request,'wganbrowser/dataset/create.html',context)
    else:
        form=datasetForm()
    context={'form':form}
    return render(request,'wganbrowser/dataset/create.html',context)

@login_required
def handle_dataset_upload(request,dataset_record,dataset_file):
    with open('/tmp/%s' % dataset_file.name,'wb+') as packed_file:
        for chunk in dataset_file.chunks():
            packed_file.write(chunk)
    return get_dataset_bundle_and_unpack(dataset_record.node_affinity,dataset_record.data_dir,dataset_file.name,DEBUG=settings.DEBUG)


@login_required
def detail(request,dataset_id):
    return HttpResponse("Looking at details for dataset</br> %s" % str(get_object_or_404(dataset,pk=dataset_id)))
