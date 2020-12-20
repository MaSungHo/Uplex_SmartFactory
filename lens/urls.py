from django.urls import path
from . import views

# 여러 app이 있을 경우 template에서 구별해내기 위한 namespace
app_name = 'lens'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:instance_id>/', views.detail, name='detail'),
    path('results/<int:instance_id>/', views.results, name='results'),
]
