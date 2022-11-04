from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(dataset)
admin.site.register(model)
admin.site.register(modelRun)
admin.site.register(modelSnapshot)
admin.site.register(library)