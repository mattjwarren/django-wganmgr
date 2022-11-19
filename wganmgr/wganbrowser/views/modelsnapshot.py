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
def detail(request,modelsnapshot_id):
    modelsnapshot=modelSnapshot.objects.get(pk=modelsnapshot_id)
    context={'modelsnapshot':modelsnapshot}
    return render (request,'wganbrowser/modelsnapshot/detail.html',context)
