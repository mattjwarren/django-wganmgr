from django.forms import ModelForm
from .models import model as modelClass

class modelForm(ModelForm):
    class Meta:
        model = modelClass
        fields = ['name','library','dataset']
