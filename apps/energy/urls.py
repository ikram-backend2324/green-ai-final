from django.urls import path
from . import views

app_name = 'energy'

urlpatterns = [
    path('', views.source_list, name='source_list'),
    path('source/add/', views.source_create, name='source_create'),
    path('source/<int:pk>/', views.source_detail, name='source_detail'),
    path('source/<int:source_pk>/reading/add/', views.reading_create, name='reading_create'),
]