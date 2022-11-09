from django.urls import path

from . import views


app_name = 'wganbrowser'
urlpatterns = [
    path('', views.model.index, name='index'),
    #/wganbrowser/models/
    path('models/',views.model.models,name='models'),
    #/wganbrowser/model/detail/{model_id}/
    path('model/detail/<int:model_id>/',views.model.detail,name='model_detail'),
    #/wganbrwoser/model/create/
    path('model/create/',views.model.create,name='model_create'),
    #/wganbrwoser/model/save/
    path('model/save/',views.model.save,name='model_save'),
    #/wganbrwoser/model/delete/
    path('model/delete/<int:model_id>/',views.model.delete,name='model_delete'),

    #/wganbrowser/dataset/detail/{dataset_id}/
    path('dataset/detail/<int:dataset_id>/',views.dataset.detail,name='dataset_detail'),

    #/wganbrowser/modelruns/
    path('modelruns/',views.modelrun.modelruns,name='modelruns'),
    #/wganbrowser/modelrun/detail/{modelrun_id}
    path('modelrun/detail/<int:modelrun_id>/',views.modelrun.detail,name='modelrun_detail'),
    #/wganbrowser/modelrun/create/
    path('modelrun/create/',views.modelrun.create,name='modelrun_create'),
    #/wganbrwoser/modelrun/save/
    path('modelrun/save/',views.modelrun.save,name='modelrun_save'),
    #/wganbrwoser/modelrun/delete/{modelrun_id}
    path('modelrun/delete/<int:modelrun_id>/',views.modelrun.delete,name='modelrun_delete'),
    #/wganbrowser/modelrun/request/{modelrun_id}
    path('modelrun/request/<int:modelrun_id>/',views.modelrun.request,name='modelrun_request'),
    #/wganbrowser/modelrun/post/
    path('modelrun/post/',views.modelrun.post,name='modelrun_post'),

    #/wganbrowser/jobs/
    path('jobs/',views.job.jobs,name='jobs'),

    #/wganbrowser/modelsnapshot_detail/{modelsnapshot_id}/
    path('modelsnapshot_detail/<int:modelsnapshot_id>/',views.modelsnapshot.modelsnapshot_detail,name='modelsnapshot_detail'),

    #/wganbrowser/library_detail/{library_id}/
    path('library_detail/<int:library_id>/',views.library.library_detail,name='library_detail'),
]