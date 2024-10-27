from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('search/', views.handle_search, name='search'),
    path('download/<path:file_path>/', views.download_summary, name='download_summary'),
]
