from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_url, name='geturl'),
    path('scraped_list/', views.scraped_list, name='scraped_list'),
    path('download_data/', views.download_data, name='download_data'),
]