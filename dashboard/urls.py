from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('bookings/', views.booking_history, name='booking_history'),
    path('favorites/', views.saved_packages, name='saved_packages'),
    path('favorites/toggle/<slug:slug>/', views.toggle_favorite, name='toggle_favorite'),
]
