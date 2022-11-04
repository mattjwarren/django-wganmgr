from django.urls import path

from . import views

urlpatterns = [
    #/wganbrowser
    path('', views.index, name='index'),
    #/wganbrowser/model/{model_id}/
    path('model/<int:model_id>/',views.model_detail,name='model_detail'),
    #/wganbrowser/model/{model_id}/
    path('dataset/<int:dataset_id>/',views.dataset_detail,name='dataset_detail'),
    #/wganbrowser/model/{model_id}/
    path('modelrun/<int:modelrun_id>/',views.modelrun_detail,name='modelrun_detail'),
    #/wganbrowser/model/{model_id}/
    path('modelsnapshot/<int:modelsnapshot_id>/',views.modelsnapshot_detail,name='modelsnapshot_detail'),
    #/wganbrowser/model/{model_id}/
    path('library/<int:library_id>/',views.library_detail,name='library_detail'),
]