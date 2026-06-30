from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('packages/', views.packages, name='packages'),
    path('package/<slug:slug>/', views.package_detail, name='package_detail'),
]
