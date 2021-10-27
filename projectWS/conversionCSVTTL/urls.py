from django.urls import path
from . import views


urlpatterns = [
    path('', views.document, name='document'),
    path('informations/', views.informations, name='informations'),
    path('download_TTL/', views.download_TTL, name='download_TTL'),
    path('informations/result/', views.result, name='result'),
    path('download_CSV/', views.download_CSV, name='download_CSV')
]