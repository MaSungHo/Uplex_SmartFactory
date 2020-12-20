from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:instance_id>/', views.detail, name='detail'),
    path('results/<int:instance_id>/', views.results, name='results'),
]
