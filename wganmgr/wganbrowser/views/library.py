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

#from . import *

@login_required
def library_detail(request,library_id):
    return HttpResponse("Looking at details for library</br> %s" % str(get_object_or_404(library,pk=library_id)))
