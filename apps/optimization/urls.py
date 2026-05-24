from django.urls import path
from . import views
app_name = 'optimization'
urlpatterns = [
    path('', views.optimization_list, name='list'),
    path('run/<int:source_pk>/', views.run_optimization_view, name='run'),
    path('result/<int:pk>/', views.result_detail, name='result_detail'),
]
