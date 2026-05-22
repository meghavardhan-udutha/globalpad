from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name='index'),
    path('access/', views.access_view, name='access'),
    path('upload/', views.upload_view, name='upload'),

    # REST API
    path('api/pad/<str:code>/', views.api_access_pad, name='api_access_pad'),
    path('api/upload/', views.api_upload_pad, name='api_upload_pad'),
    path('api/file/<int:file_id>/download/', views.api_download_file, name='api_download_file'),
]
