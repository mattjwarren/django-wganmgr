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
import re
import os
from .package_global import *



@login_required
def libraries(request):
    libraries=library.objects.all()
    libraries=group_records_by_field(libraries,['node_affinity'])
    context={'libraries':libraries}
    return render(request,'wganbrowser/library/libraries.html',context)

@login_required
def detail(request,library_id):
    lib=library.objects.get(pk=library_id)
    context={'library':lib}
    return render(request,"wganbrowser/library/detail.html",context)


@login_required
def edit(request,library_id):
    lib=library.objects.get(pk=library_id)
    old_full_path=lib.full_path()

    context={'library':lib,
             'action':'edit'}

    if request.method=='POST':
        form=libraryCreateEditForm(request.POST,instance=lib)
        if form.is_valid():
            data=form.cleaned_data
            if not data['node_affinity'] in settings.JENKINS_TRAINING_NODES:
                context.update({'message': LIBRARY_STORAGE_NODE_UNKNOWN % data['node_affinity']})
                return render(request,'wganbrowser/library/create_edit.html',context)
            
            if bad_chars_in_path(data['path']):
                context.update({'form':form,
                                'message': LIBRARY_BAD_CHARS_IN_PATH})
                return render(request,'wganbrowser/library/create_edit.html',context)                

            if data['path'].startswith('/'):
                context.update({'message': LIBRARY_ABSOLUTE_PATH})
                return render(request,'wganbrowser/library/create_edit.html',context)

            new_full_path=os.path.join(settings.NODE_STORAGE_ROOT,data['path'],"")

            if does_path_exist_on_node(data['node_affinity'],new_full_path):
                context.update({'message': LIBRARY_PATH_ALREADY_USED % data['path']})
                return render(request,'wganbrowser/library/create_edit.html',context)

            if not move_path(data['node_affinity'],old_full_path,new_full_path):
                context.update({'message': LIBRARY_PATH_COULD_NOT_MOVE % (data['node_affinity'],old_full_path,full_path)})
                return render(request,'wganbrowser/library/create_edit.html',context)
            
            lib.name=data['name']
            lib.path=data['path']
            lib.node_affinity=data['node_affinity']
            lib.save()

            return libraries(request)
    else:
        form=libraryCreateEditForm(instance=lib)
    context.update({'form':form})
    return render(request,'wganbrowser/library/create_edit.html',context)

@login_required
def delete(request,library_id):
    lib=library.objects.get(pk=library_id)
    lib.delete()
    return libraries(request)

@login_required
def create(request):
    context={'action':'create'}

    if request.method == 'POST':
        form=libraryCreateEditForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            context.update({'form':form})

            if not data['node_affinity'] in settings.JENKINS_TRAINING_NODES:
                context.update({'message': LIBRARY_STORAGE_NODE_UNKNOWN % data['node_affinity']})
                return render(request,'wganbrowser/library/create_edit.html',context)
            
            if bad_chars_in_path(data['path']):
                context.update({'message': LIBRARY_BAD_CHARS_IN_PATH})
                return render(request,'wganbrowser/library/create_edit.html',context)                

            if data['path'].startswith('/'):
                context.update({'message': LIBRARY_ABSOLUTE_PATH})
                return render(request,'wganbrowser/library/create_edit.html',context)

            new_full_path=os.path.join(settings.NODE_STORAGE_ROOT,data['path'],"")

            if does_path_exist_on_node(data['node_affinity'],new_full_path):
                context.update({'message': LIBRARY_PATH_ALREADY_USED % data['path']})
                return render(request,'wganbrowser/library/create_edit.html',context)

            #try and create
            if not create_path_on_node(data['node_affinity'],new_full_path):
                context.update({'message': LIBRARY_PATH_COULD_NOT_CREATE % data['path']})
                return render(request,'wganbrowser/library/create_edit.html',context)

            new_library=library(name=data['name'],
                                path=data['path'],
                                node_affinity=data['node_affinity'])
            new_library.save()

            return libraries(request)
    else:
        form=libraryCreateEditForm()
    context.update({'form':form})
    return render(request,'wganbrowser/library/create_edit.html',context)

