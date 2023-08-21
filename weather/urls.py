from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('info/', views.info_view, name='info'),
]
