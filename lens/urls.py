from django.urls import path
from . import views

# 여러 app이 있을 경우 template에서 구별해내기 위한 namespace
app_name = 'lens'
urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('image/', views.image, name='image'),
    path('lens/', views.create, name='create'),
    path('decision/', views.decision, name='decision'),
    path('results/<int:instance_id>/', views.results, name='results'),
]
