# images/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('img/', views.random_wallhaven_image, name='random_wallhaven_image'),
    path('img_file/', views.random_wallhaven_image_file, name='random_wallhaven_image_file'),
]
