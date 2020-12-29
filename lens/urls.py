from django.urls import path
from . import views

# 여러 app이 있을 경우 template에서 구별해내기 위한 namespace
app_name = 'lens'
urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('image/select/', views.select, name='select'),
    path('image/single/', views.single_image, name='single_image'),
    path('image/group/', views.group_images, name='group_image'),
    path('single/decision/', views.decision, name='decision'),
    path('group/decision/', views.decisions, name='decisions'),
    path('search/', views.search, name='search'),
    path('results/', views.results, name='results'),
    path('delete/', views.delete, name='delete')
]
