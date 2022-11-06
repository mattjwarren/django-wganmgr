from django.urls import path

from . import views

app_name = 'wganbrowser'
urlpatterns = [
    path('', views.index, name='index'),
    #/wganbrowser/models/
    path('models/',views.models,name='models'),
    #/wganbrowser/model_detail/{model_id}/
    path('model_detail/<int:model_id>/',views.model_detail,name='model_detail'),
    #/wganbrwoser/model_create/
    path('model_create/',views.model_create,name='model_create'),
    #/wganbrwoser/model_save/
    path('model_save/',views.model_save,name='model_save'),
    #/wganbrwoser/model_delete/
    path('model_delete/<int:model_id>/',views.model_delete,name='model_delete'),
    #/wganbrowser/dataset_detail/{dataset_id}/
    path('dataset_detail/<int:dataset_id>/',views.dataset_detail,name='dataset_detail'),
    #/wganbrowser/modelrun_detail/{modelrun_id}/
    path('modelrun_detail/<int:modelrun_id>/',views.modelrun_detail,name='modelrun_detail'),
    #/wganbrowser/modelsnapshot_detail/{modelsnapshot_id}/
    path('modelsnapshot_detail/<int:modelsnapshot_id>/',views.modelsnapshot_detail,name='modelsnapshot_detail'),
    #/wganbrowser/library_detail/{library_id}/
    path('library_detail/<int:library_id>/',views.library_detail,name='library_detail'),
]