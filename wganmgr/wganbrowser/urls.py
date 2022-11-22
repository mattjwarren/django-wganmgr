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
    path('job/jobs/',views.job.jobs,name='jobs'),
    #/wganbrowser/job/detail/modelrun_id/node_name/
    path('job/detail/<int:modelrun_id>/<str:node_name>/',views.job.detail,name='job_detail'),
    #/wganbrowser/job/detail/modelrun_id/node_name/
    path('job/halt/<int:modelrun_id>/<str:node_name>/',views.job.halt,name='job_halt'),
    #/wganbrowser/job/upload_snapshot/modelrun_id/node_name/
    path('job/upload_snapshot/<int:modelrun_id>/<str:node_name>/',views.job.force_model_snapshot,name='job_upload_snapshot'),
    #/wganbrowser/job/console_log/modelrun_id/node_name/
    path('job/console_log/<int:modelrun_id>/<str:node_name>/',views.job.console_log,name='job_console_log'),
    

    #/wganbrowser/modelsnapshot/detail/{modelsnapshot_id}/
    path('modelsnapshot/detail/<int:modelsnapshot_id>/',views.modelsnapshot.detail,name='modelsnapshot_detail'),

    #/wganbrowser/library/libraries/
    path('library/libraries/',views.library.libraries,name='libraries'),
    #/wganbrowser/library/detail/{library_id}/
    path('library/detail/<int:library_id>/',views.library.detail,name='library_detail'),
    #/wganbrowser/library/edit/{library_id}/
    path('library/edit/<int:library_id>/',views.library.edit,name='library_edit'),
    #/wganbrowser/library/delete/{library_id}/
    path('library/delete/<int:library_id>/',views.library.delete,name='library_delete'),
    #/wganbrowser/library/create/{library_id}/
    path('library/create/',views.library.create,name='library_create'),

]