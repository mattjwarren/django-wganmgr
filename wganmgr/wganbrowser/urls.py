from django.urls import path

from . import views


app_name = 'wganbrowser'
urlpatterns = [
    path('', views.model.index, name='index'),
    #/wganbrowser/models/
    path('models/',views.model.models,name='models'),
    #/wganbrowser/model_detail/{model_id}/
    path('model_detail/<int:model_id>/',views.model.detail,name='model_detail'),
    #/wganbrwoser/model_create/
    path('model_create/',views.model.model_create,name='model_create'),
    #/wganbrwoser/model_save/
    path('model_save/',views.model.model_save,name='model_save'),
    #/wganbrwoser/model_delete/
    path('model_delete/<int:model_id>/',views.model.model_delete,name='model_delete'),

    #/wganbrowser/dataset_detail/{dataset_id}/
    path('dataset_detail/<int:dataset_id>/',views.dataset.dataset_detail,name='dataset_detail'),

    #/wganbrowser/modelruns/
    path('modelruns/',views.modelrun.modelruns,name='modelruns'),
    #/wganbrowser/modelrun_details/{modelrun_id}
    path('modelrun_detail/<int:modelrun_id>/',views.modelrun.modelrun_detail,name='modelrun_detail'),
    #/wganbrowser/modelrun_create/
    path('modelrun_create/',views.modelrun.modelrun_create,name='modelrun_create'),
    #/wganbrwoser/model_save/
    path('modelrun_save/',views.modelrun.modelrun_save,name='modelrun_save'),
    #/wganbrwoser/modelrun_delete/
    path('modelrun_delete/<int:modelrun_id>/',views.modelrun.modelrun_delete,name='modelrun_delete'),
    #/wganbrowser/modelrun_request/{modelrun_id}
    path('modelrun_request/<int:modelrun_id>/',views.modelrun.modelrun_request,name='modelrun_request'),
    #/wganbrowser/modelrun_post/
    path('modelrun_post/',views.modelrun.modelrun_post,name='modelrun_post'),

    #/wganbrowser/jobs/
    path('jobs/',views.jobs.jobs,name='jobs'),

    #/wganbrowser/modelsnapshot_detail/{modelsnapshot_id}/
    path('modelsnapshot_detail/<int:modelsnapshot_id>/',views.modelsnapshot.modelsnapshot_detail,name='modelsnapshot_detail'),

    #/wganbrowser/library_detail/{library_id}/
    path('library_detail/<int:library_id>/',views.library.library_detail,name='library_detail'),
]