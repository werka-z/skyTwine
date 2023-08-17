from django.urls import path
from . import views

urlpatterns = [
    path('', views.ow_view, name='index'),
    path('ow/', views.ow_view, name='ow'),
    path('wa/', views.wa_view, name='wa'),
    path('average/', views.average_view, name='average'),
    path('info/', views.info_view, name='info'),
]
