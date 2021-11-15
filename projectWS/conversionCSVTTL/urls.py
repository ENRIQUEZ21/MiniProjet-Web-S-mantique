from django.urls import path
from . import views


urlpatterns = [
    path('', views.document, name='document'), # To go to the page of the first form
    path('informations/', views.informations, name='informations'), # To go to the page of the second form
    path('download_TTL/', views.download_TTL, name='download_TTL'), # To download TTL file of result
    path('informations/result/', views.result, name='result'), # To go to the final page 
    path('download_CSV/', views.download_CSV, name='download_CSV') # To download the CSV file uploaded
]