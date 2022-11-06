from django.urls import path

from . import views

urlpatterns = [
    #/wganbrowser
    path('', views.index, name='index'),
    #/wganbrowser/model/{model_id}/
    path('model_detail/<int:model_id>/',views.model_detail,name='model_detail'),
    #/wganbrowser/model/{model_id}/
    path('dataset_detail/<int:dataset_id>/',views.dataset_detail,name='dataset_detail'),
    #/wganbrowser/model/{model_id}/
    path('modelrun_detail/<int:modelrun_id>/',views.modelrun_detail,name='modelrun_detail'),
    #/wganbrowser/model/{model_id}/
    path('modelsnapshot_detail/<int:modelsnapshot_id>/',views.modelsnapshot_detail,name='modelsnapshot_detail'),
    #/wganbrowser/model/{model_id}/
    path('library_detail/<int:library_id>/',views.library_detail,name='library_detail'),
]