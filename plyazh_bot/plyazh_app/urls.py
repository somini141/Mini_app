from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_request/', views.submit_request, name='submit_request'),
]