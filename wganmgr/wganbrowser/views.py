from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the wgan browser index.")

def model_detail(request,model_id):
    return HttpResponse("Looking at details for model %s" % model_id)

def dataset_detail(request,dataset_id):
    return HttpResponse("Looking at details for dataset %s" % dataset_id)

def modelrun_detail(request,modelrun_id):
    return HttpResponse("Looking at details for modelrun %s" % modelrun_id)

def modelsnapshot_detail(request,modelsnapshot_id):
    return HttpResponse("Looking at details for modelsnapshot %s" % modelsnapshot_id)

def library_detail(request,library_id):
    return HttpResponse("Looking at details for library %s" % library_id)

